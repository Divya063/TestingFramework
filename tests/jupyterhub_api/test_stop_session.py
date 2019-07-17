
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
from SessionUtils import Test, JupyterhubTest
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import yaml


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", dest="port", type=int,
                        required = True,
                        )
    parser.add_argument( "--users", nargs='+', dest="users",
                        required  = True,
                        help='list of users')
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

    def __init__(self, port, users, base_path, verify):
        JupyterhubTest.__init__(self, port, base_path, verify)
        self.ref_test_name = "Check_Sessions"
        self.users = users
        super().log_params()
        self.exit = 0


    def stop_session(self):
        self.log.write("info", "Terminating the sessions")
        global r
        for user in self.users:
            try:
                r = super().api_calls("delete", user, endpoint ="users/server")

            except requests.exceptions.RequestException as e:
                self.log.write("error", str(e))
                self.exit |= 1

            else:
                if (r.status_code == 204):
                    self.log.write("info", user + " server was removed")
                else:
                    self.log.write("error", user + " server was not removed")
                    self.exit |= 1

        return self.exit

    def exit_code(self):
        self.exit|=self.stop_session()
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_stop_session = StopSession(args.port, args.users, args.base, verify = False)
    (test_stop_session.exit_code())
