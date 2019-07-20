import json
import requests
import subprocess
import os
import sys
import argparse

sys.path.append("..")
import time
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from jupyterhubtest import JupyterhubTest
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", dest="port", type=int,
                        required=True,
                        )

    parser.add_argument("--token", dest="token",
                        required=False,
                        help='token')

    parser.add_argument("--base_path", dest="base",
                        required=False,
                        help='base path')

    args = parser.parse_args()
    return args


class CheckAPI(JupyterhubTest):
    """Test if an api is reachable"""

    def __init__(self, port, token, base_path, verify):
        self.ref_test_name = "APIReachable"
        JupyterhubTest.__init__(self, port, token, base_path, verify)

    def check_api(self):
        try:
            r = super().call_api("get")

        except requests.exceptions.RequestException as e:
            self.log.write("error", str(e))
            self.exit = 1
        else:
            if r.status_code == 200:
                self.exit = 0
                self.log.write("info", "API is reachable")
            else:
                self.log.write("error", "API is not reachable")
                self.exit = 1
        return self.exit

    def exit_code(self):
        self.exit = self.check_api()
        self.log.write("info", "overall exit code " + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_web_reachable = CheckAPI(args.port, args.token, args.base, False)
    (test_web_reachable.exit_code())
