import json
import requests
import subprocess
import os
import sys

sys.path.append("..")
import yaml
import time
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
import argparse
from jupyterhubtest import JupyterhubTest
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
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


class CheckSession(JupyterhubTest):
    """
    Test if a session is running

    To run the test use the following command:
    python3 test_check_session.py --port 443 --users user1 --base_path ""

    For multiple users

    python3 test_check_session.py --port 443 --users user0 user1 user2 --base_path ""

    """

    def __init__(self, port, token, users, base_path, verify):
        self.ref_test_name = "Check_Sessions"
        super().__init__(port, token, base_path, verify)
        self.users = users

    def check_container(self, user):
        """Checks if a container is running"""

        s = subprocess.check_output('docker ps', shell=True)
        container_name = "jupyter-" + user
        if s.decode("utf-8").find(container_name) == -1:
            self.log.write("error", "Container is not running")
            return 1

    def check_session(self):

        # Submit a  get request to  https://localhost:443/hub/api/users/user1, this will return the information
        # of particular user in json format, check the value of the field 'server' if it is null server is not active
        #
        # Example:
        #     json of user having active server-
        #     {"kind": "user", "name": "user1", "admin": false, "groups": [], "server": "/user/user1/", "pending": null,
        #     }
        #
        #     json of user have non-active server -
        #     {"kind": "user", "name": "user3", "admin": false, "groups": [], "server": null, "pending": null}

        for user in self.users:
            try:
                r = self.call_api("get", user)

            except requests.exceptions.RequestException as e:
                self.log.write("error", str(e))
                return 1
            else:
                if r.status_code == 200:
                    status = r.json()
                    server_status = status['server']
                    check_container = self.check_container(user)
                    self.log.write("info", "exit code : check_container " + str(check_container))
                    if server_status and check_container != 1:
                        self.log.write("info", user + " server is present at " + server_status)
                        return 0
                    else:
                        self.log.write("error", user + " server is not present ")
                        return 1
                else:
                    self.log.write("error", r.content.decode('utf-8'))
                    return 1

    def exit_code(self):
        self.exit = self.check_session()
        self.log.write("info", "exit code %s" % self.exit)

        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_active_session = CheckSession(args.port, args.token, args.users, args.base, verify=False)
    (test_active_session.exit_code())
