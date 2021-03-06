import json
import requests
import subprocess
import os
import docker
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


class Token(JupyterhubTest):
    """
    Test the vailidity of token

    To run the test use the following command:
    python3 test_token.py --port 443 --users user1 --base_path ""

    For multiple users

    python3 test_token.py --port 443 --users user0 user1 user2 --base_path ""

    """

    def __init__(self, hostname, port, token, users, base_path, verify):
        self.ref_test_name = "Check_Token"
        super().__init__(hostname, port, token, base_path, verify)
        self.users = users

    def run_test(self):

        # Submit a  get request to  https://localhost:443/hub/api/users/user{} to check if a token is valid or not
        exit_code = 0
        error_codes = [403, 404, 405]
        for user in self.users:
            try:
                r = self.call_api("get", user)

            except requests.exceptions.RequestException as e:
                self.log.write("error", str(e))
                exit_code = 1
                self.log.write("info", "overall exit code" + str(exit_code))
                return 1

            else:
                if r.status_code in error_codes:
                    self.log.write("error", r.content.decode('utf-8'))
                    exit_code = 1
                else:
                    self.log.write("info", "token is valid")
                    self.log.write("info", user + " info " + r.content.decode('utf-8'))

        self.log.write("info", "overall exit code " + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_active_session = Token(args.hostname, args.port, args.token, args.users, args.base, verify=False)
    (test_active_session.run_test())
