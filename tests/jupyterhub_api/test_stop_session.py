import json
import requests
import subprocess
import os
import time
import argparse
import sys

sys.path.append("..")
import time
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from jupyterhubtest import JupyterhubTest
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--hostname", dest="hostname", required=True)
    parser.add_argument("--port", dest="port", type=int,
                        required=True,
                        )
    parser.add_argument("--users", nargs='+', dest="users",
                        required=True,
                        help='list of users')
    parser.add_argument("--token", dest="token",
                        required=False,
                        help='token')
    parser.add_argument("--base_path", dest="base",
                        required=False,
                        help='base path')

    args = parser.parse_args()
    return args


class StopSession(JupyterhubTest):
    """
    Test to stop the session

    To run the test use the following command:
    python3 test_stop_session.py --port 443 --users user1 --base_path ""

    For multiple users

    python3 test_stop_session.py --port 443 --users user0 user1 user2 --base_path ""

    """

    def __init__(self, hostname, port, token, users, base_path, verify):
        self.ref_test_name = 'Stop_Session'
        super().__init__(hostname, port, token, base_path, verify)
        self.users = users

    def run_test(self):
        self.log.write("info", "Terminating the sessions")
        exit_code = 0
        for user in self.users:
            try:
                # Makes a request to stop the server
                r = self.call_api("delete", user, endpoint="/server")

            except requests.exceptions.RequestException as e:
                self.log.write("error", str(e))
                exit_code = 1

            else:
                check_container = self.check_container(user)
                # Checks if the request has been successfully submitted also
                # checks if the container is present or not
                if r.status_code == 204 and check_container == 1:
                    self.log.write("info", user + " server was removed")
                else:
                    self.log.write("error", user + " server was not removed")
                    self.log.write("error", r.content.decode('utf-8'))
                    exit_code = 1

        self.log.write("info", "overall exit code " + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_stop_session = StopSession(args.hostname, args.port, args.token, args.users, args.base, verify=False)
    (test_stop_session.run_test())
