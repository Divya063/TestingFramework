
import json
import requests
import subprocess
import os
from SessionUtils import CreateSession
import time
import argparse
import sys
sys.path.append("..")
import time
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", dest="port", type=int,
                        required = True,
                        )
    parser.add_argument( "--users", nargs='+', dest="users",
                        required  = True,
                        help='list of users')
    parser.add_argument("--path", dest="path",
                        required=True,
                        help = 'Path where config file exists')
    args = parser.parse_args()
    return args

class StopSession:
    def __init__(self, port, users, path):
        self.port = port
        self.users = users
        self.path = path
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.ref_test_name =""
        self.exit = 0
        self.token = ""
        self.session = CreateSession(port, users, path)
        self.ref_timestamp = int(time.time())
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder,
                                       self.ref_test_name + "_" + time.strftime("%Y-%m-%d_%H:%M:%S") + LOG_EXTENSION))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)



    def create_session(self):

        try:
            self.token, command = self.session.create_token()
            self.log.write("info", "created token..")
            self.log.write("info", "Creating Users..")
            for user in self.users:
                self.session.create_users(user)
                self.log.write("info", "Created " + user)
            self.log.write("info", "Creating Servers..")
            for user in self.users:
                self.session.create_server(user)
                time.sleep(30)
                self.log.write("info", "Created " + user + " session")
        except requests.exceptions.RequestException as e:
            self.log.write("error", str(e))
            self.exit |= 1

        except Exception as e:
            self.log.write("error", str(e))
            self.exit |= 1
        else:
            self.log.write("info", "Session successfully created")

        return self.exit


    def check_running_session(self):
        self.log.write("info", "checking if session is running or not")
        for user in self.users:
                try:
                    check_session = self.session.create_server(user)

                except requests.exceptions.RequestException as e:
                    self.log.write("error", str(e))
                    self.exit |= 1
                else:
                    if(check_session.status_code ==400):
                        self.log.write("info", user + " session exists and running")
                    else:
                        self.log.write("error", user + " session does not exist")
                        self.exit |= 1
        return self.exit




    def stop_session(self):
        self.log.write("info", "Terminating the sessions")
        global r
        for user in self.users:
            try:
                r = requests.delete(self.main_url + 'users/%s' % user + "/server",
                                  headers={
                                      'Authorization': 'token %s' % self.token,
                                  },
                                  verify=False
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
        self.exit |= self.create_session()
        self.exit |= self.check_running_session()
        if(self.exit !=1):
            self.exit|=self.stop_session()
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_stop_session = StopSession(args.port, args.users, args.path)
    print(test_stop_session.exit_code())



