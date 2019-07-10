"""

Test to stop the session

To run the test use the following command:
python3 test_stop_session.py --port 443 --users user1

For multiple users

python3 test_stop_session.py --port 443 --users user0 user1 user2

"""
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
from SessionUtils import Tokens
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

    args = parser.parse_args()
    return args

class StopSession:
    def __init__(self, port, users, verify):
        self.port = port
        self.users = users
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.ref_test_name ="Stop_Session"
        self.exit = 0
        self.verify = verify
        self.session = Tokens()
        self.token = self.session.get_tokens()
        print(self.token)
        self.ref_timestamp = int(time.time())
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder,
                                       self.ref_test_name + "_" + time.strftime("%Y-%m-%d_%H:%M:%S") + LOG_EXTENSION))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)


    def get_tokens(self):
        """
        Get token from yaml file
        """
        path = os.path.join('/', 'test.yaml')
        #path = "/".join(script_directory) + "/" + 'test.yaml'
        if os.path.exists(path):
            with open(path) as f:
                tasks = yaml.safe_load(f)
                #print(tasks)

            test_jupyterhub = tasks['tests']['jupyterhub_api']
            self.token = test_jupyterhub['create_session']['token']
            #print(self.token)


    def stop_session(self):
        self.log.write("info", "Terminating the sessions")
        global r
        for user in self.users:
            try:
                r = requests.delete(self.main_url + 'users/%s' % user + "/server",
                                  headers={
                                      'Authorization': 'token %s' % self.token,
                                  },
                                  verify= self.verify
                              )

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
    test_stop_session = StopSession(args.port, args.users, verify = False)
    (test_stop_session.exit_code())
