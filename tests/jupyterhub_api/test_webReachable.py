"""
Test if a api is reachable
"""

import json
import requests
import subprocess
import os
import docker
import sys
sys.path.append("..")
import time
from logger import Logger, LOG_FOLDER, LOG_EXTENSION

import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", dest="port", type=int,
                        required = True,
                        )
    args = parser.parse_args()
    return args


class webReachable:
    def __init__(self, port):
        self.port = port
        self.exit =0
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.ref_test_name= "WebReachable"
        self.ref_timestamp = int(time.time())
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)

    def check_api(self):
        try:
            r = requests.get(self.main_url, verify=False)

        except requests.exceptions.RequestException as e:
            self.log.write("error", str(e))
            self.exit |= 1
        else:
            if(r.status_code ==200):
                self.log.write("info", "API is reachable")
            else:
                self.log.write("error", "API is not reachable")
                self.exit |= 1
        return self.exit




    def exit_code(self):
        self.exit |= self.check_api()
        self.log.write("info", "overall exit code " + str(self.exit) )
        return self.exit

if __name__ == "__main__":
    args = get_args()
    test_web_reachable = webReachable(args.port)
    (test_web_reachable.exit_code())








