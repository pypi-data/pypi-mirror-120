#   Copyright Peznauts <kevin@cloudnull.com>. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import json
import time

from directord import components


class Coordination:
    """Coordination connection context manager."""

    def __init__(self, driver, log, job_id):
        """Initialize the coordination context manager class."""

        self.driver = driver
        self.bind_backend = self.driver.backend_connect()
        self.log = log
        self.job_id = job_id

    def __enter__(self):
        """Return the bind_backend object on enter."""

        self.log.debug(
            "Coordination started to %s for job [ %s ]",
            self.driver.identity,
            self.job_id,
        )
        return self.bind_backend

    def __exit__(self, *args, **kwargs):
        """Close the bind coordination object."""

        try:
            self.bind_backend.close(linger=2)
            count = 0
            while not self.bind_backend.closed:
                count += 1
                if count > 60:
                    raise TimeoutError(
                        "Job [ {} ] failed to close coordination"
                        " socket".format(self.job_id)
                    )
                else:
                    self.bind_backend.close(linger=2)
                    self.delay(1)
        except Exception as e:
            self.log.error(
                "Job [ %s ] coordination ran into an exception"
                " while closing the socket %s",
                str(e),
                self.job_id,
            )
        else:
            self.log.debug(
                "Job [ %s ] coordination socket closed", self.job_id
            )

        self.log.debug(
            "Coordination ended for %s for job [ %s ]",
            self.driver.identity,
            self.job_id,
        )
        time.sleep(0.25)


class Component(components.ComponentBase):
    def __init__(self):
        """Initialize the component cache class."""

        super().__init__(desc="Process coordination commands")
        self.requires_lock = True

    def args(self):
        """Set default arguments for a component."""

        super().args()
        self.parser.add_argument(
            "sha",
            help=("job sha to be completed."),
        )
        self.parser.add_argument(
            "--job-timeout",
            help=(
                "Wait for %(default)s seconds for a given item to be present"
                " in cache."
            ),
            default=600,
            type=int,
        )
        self.parser.add_argument(
            "--identity",
            help=(
                "Worker identities to search for a specific job item."
                " When an identity is defined, the lookup will search the"
                " defined identities for the item. JOB_WAIT will block"
                " until the `item` is found in all specified identities."
                " this value can be used multiple times to express many"
                " identities."
            ),
            metavar="STRING",
            nargs="+",
            required=True,
        )

    def server(self, exec_array, data, arg_vars):
        """Return data from formatted cacheevict action.
        :param exec_array: Input array from action
        :type exec_array: List
        :param data: Formatted data hash
        :type data: Dictionary
        :param arg_vars: Pre-Formatted arguments
        :type arg_vars: Dictionary
        :returns: Dictionary
        """

        super().server(exec_array=exec_array, data=data, arg_vars=arg_vars)
        data["job_sha"] = self.known_args.sha
        data["job_timeout"] = self.known_args.job_timeout
        data["identity"] = self.known_args.identity
        return data

    def client(self, cache, job):
        """Run file transfer operation.

        :param cache: Caching object used to template items within a command.
        :type cache: Object
        :param job: Information containing the original job specification.
        :type job: Dictionary
        :returns: tuple
        """

        driver = self.driver.__copy__()
        self.log.debug("client(): job: %s, cache: %s", job, cache)
        with Coordination(
            driver=driver, log=self.log, job_id=job["job_id"]
        ) as bind_backend:
            return self._client(cache, job, driver, bind_backend)

    def _client(self, cache, job, driver, bind_backend):
        """Run cache query_wait command operation.
        :param cache: Caching object used to template items within a command.
        :type cache: Object
        :param job: Information containing the original job specification.
        :type job: Dictionary
        :param driver: Connection object used to store information used in a
                     return message.
        :type driver: Object
        :returns: tuple
        """

        start_time = time.time()
        confirmed_identities = set()
        driver.socket_send(
            socket=bind_backend,
            msg_id=job["job_id"].encode(),
            control=driver.coordination_notice,
            command=job["job_sha"].encode(),
            data=json.dumps(
                [i for i in job["identity"] if i is not driver.identity]
            ).encode(),
        )
        self.log.debug("Job [ %s ] coordination notice sent", job["job_id"])
        while (time.time() - start_time) < job["job_timeout"]:
            if driver.bind_check(bind=bind_backend, constant=512):
                (
                    msg_id,
                    control,
                    command,
                    _,
                    info,
                    _,
                    _,
                ) = driver.socket_recv(socket=bind_backend)
                self.log.debug(
                    "Received backend message for job [ %s ]"
                    " control [ %s ]",
                    msg_id.decode(),
                    control.decode(),
                )
                if control == driver.coordination_notice:
                    self.log.debug(
                        "Job [ %s ] coordination notice received from [ %s ]",
                        msg_id.decode(),
                        info.decode(),
                    )
                    if cache.get(command.decode()) in [
                        driver.job_end.decode(),
                        driver.job_failed.decode(),
                    ]:
                        driver.socket_send(
                            socket=bind_backend,
                            msg_id=msg_id,
                            control=driver.coordination_ack,
                            info=info,
                        )
                        self.log.debug(
                            "Job [ %s ] coordination complete for [ %s ]",
                            msg_id.decode(),
                            info.decode(),
                        )
                elif control == driver.coordination_ack:
                    if info.decode() in job["identity"]:
                        self.log.debug(
                            "Job [ %s ] coordination acknowledged from"
                            " [ %s ]",
                            msg_id.decode(),
                            info.decode(),
                        )
                        confirmed_identities.add(info.decode())
                    else:
                        self.log.warning(
                            "Job [ %s ] coordination acknowledgement from"
                            " [ %s ] was not found in our expected identities"
                            " %s",
                            msg_id.decode(),
                            info.decode(),
                            job["identity"],
                        )

                elif control == driver.job_failed:
                    return (
                        None,
                        "Failed to coordinate with target identity"
                        " [ {} ]".format(info.decode()),
                        False,
                        None,
                    )
                else:
                    self.log.critical(
                        "Unknown control received [ %s ] from [ %s ]",
                        control,
                        info.decode(),
                    )
            else:
                self.log.debug(
                    "Job [ %s ] no coordination message received",
                    job["job_id"],
                )

            if sorted(confirmed_identities) == sorted(job["identity"]):
                return (
                    "Job completed",
                    None,
                    True,
                    "Job [ {} ] found SHA [ {} ] completed on all"
                    " coordinated targets: {}".format(
                        job["job_id"], job["job_sha"], job["identity"]
                    ),
                )

        return (
            None,
            "Timeout after {} seconds".format(job["job_timeout"]),
            False,
            "Job {} was never found in a completed state".format(job["sha"]),
        )
