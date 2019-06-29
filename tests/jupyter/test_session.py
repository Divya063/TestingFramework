"""
Create a session
"""

"""
To run the test run the following command:
python3 test_session.py --port 443 --users user1 --path srv/jupyterhub

For multiple users

python3 test_session.py --port 443 --users user0 user1 user2 --path srv/jupyterhub

"""


import json
import requests
import subprocess
import os
import argparse
import sys
sys.path.append("..")
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from SessionUtils import CreateSession
import time


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


class Session:
    def __init__(self, port, users, configfile):
        self.port = port
        self.users = users
        self.configfile = configfile
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.ref_test_name = "Session creation test"
        self.exit = 0
        self.token = ""
        self.ref_timestamp = int(time.time())
        self.session = CreateSession(self.port, users, self.configfile)
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))


    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)

    def check_create_token(self):
        self.log.write("info", "creating tokens..")
        global command
        try:
            self.token, command =self.session.create_token()
        except subprocess.CalledProcessError as err:
            self.log.write("error", str(err))
            self.exit|=1
        else:
            self.log.write("info", "Successfully created token " + str(self.token))
        self.log.write("info", "Exit code "+ str(self.exit))
        return self.exit


    def check_create_users(self):

        """
        Inside container
        port = 443

        Ouside container
        port = 8443
        """
        self.log.write("info", "creating users..")
        print(self.users)
        for user in self.users:
            global r
            try:
                r = self.session.create_users(user)
            except Exception as err:
                self.exit |= 1
                self.log.write("error", str(err))
                self.log.write("error", str(r))
            else:
                if r.status_code == 201:
                    self.log.write("info", user + " successfully created")
                else:
                    self.log.write("error", (r.content).decode('utf-8'))
                    self.exit|=1
        self.log.write("info", "Exit code " + str(self.exit))

        return self.exit

    def check_create_sessions(self):
        self.log.write("info", "creating sessions..")
        for user in self.users:
            global r
            try:
                r = self.session.create_sessions(user)
            except Exception as err:
                self.exit |= 1
                self.log.write("error", "status code " + str(r.status_code) + " " + str(err))

            else:
                if r.status_code == 202:
                    self.log.write("info", "Successfully requested the session")
                    """
                     After creation of sessions server needs to respond within 30 seconds otherwise there will 
                     Timeout Error
                     Example:
        
                     TimeoutError: Server at http://172.18.0.15:8888/user/user0/ didn't respond in 30 seconds
                     So, even after a successful request a session may not be created
                    """
                    time.sleep(30)

                    """
                    Try to create a same session again, a conflict request for creating a session returns  400 status code 
                    An example from log:
                    
                    [W 2019-06-29 14:46:20.850 SWAN web:1782] 400 POST /hub/api/users/user1/server (::ffff:127.0.0.1): user1 is already running
                    """
                    check_session = self.session.create_sessions(user)
                    if(check_session.status_code==409 or check_session.status_code==400):
                        self.log.write("info", "Successfully created the" + user + " session")

                    else:
                        self.log.write("error",  user + " session was not created")
                        self.exit |= 1
                elif r.status_code == 201:
                    """
                    Sometimes session are created without any wait time
                    """
                    self.log.write("info", "Successfully created the" + user + " session")

                else:
                    self.log.write("error", user + " session was not created")
                    self.log.write("error", "status code " + str(r.status_code) + " " + (r.content).decode('utf-8'))
                    self.exit |= 1

        return self.exit


    def exit_code(self):
        self.exit |= self.check_create_token()
        self.exit |= self.check_create_users()
        self.exit|= self.check_create_sessions()
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_session = Session(args.port, args.users, args.path)
    (test_session.exit_code())


