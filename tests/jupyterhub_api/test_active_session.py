"""
Test if a session is running
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
from SessionUtils import CreateSession

import argparse

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


class ActiveSession:
    def __init__(self, port, users, path):
        self.users = users
        self.port = port
        self.exit =0
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.ref_test_name= "Active_Sessions"
        self.session = CreateSession(port, users, path)
        self.ref_timestamp = int(time.time())
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)

    def create_session(self):

        try:
            self.session.create_token()
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
            self.exit |=1

        except Exception as e:
            self.log.write("error", str(e))
            self.exit |= 1
        else:
            self.log.write("info", "Session successfully created")

        return self.exit

    def check_session(self):

            """
            One method could be:
            check if user container is up and running

            s = subprocess.check_output('docker ps', shell=True)
            sessions_not_running = set()
            for user in self.user:
                container_name = "jupyterhub_api-" + user
            if(s.decode("utf-8").find(container_name) == -1):
                sessions_not_running.add(user)
                self.exit|=1

            Second method:

            Submit a post request to /hub/api/users/{username}/server which will in return
            result in 400 status code(conflict) as the server is already running

            """
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



    def exit_code(self):
        if(self.create_session()==0):
            self.exit |= self.check_session()

        return self.exit

if __name__ == "__main__":
    args = get_args()
    test_active_session = ActiveSession(args.port, args.users, args.path)
    print(test_active_session.exit_code())








