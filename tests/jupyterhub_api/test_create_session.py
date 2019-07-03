"""
Create a session
"""

"""
To run the test run the following command:

python3 test_create_session.py --port 443 --users user1 --path /srv/jupyterhub 
--token {token value} --data 
{'LCG-rel': 'LCG_95a', 'platform': 'x86_64-centos7-gcc7-opt', 'scriptenv': 'none', 'ncores': 2,
'memory': 8589934592, 'spark-cluster': 'none'}


For multiple users

python3 test_create_session.py --port 443 --users user0 user1 user2 --path /srv/jupyterhub 
--token {token value} --data                                                                  
{'LCG-rel': 'LCG_95a', 'platform': 'x86_64-centos7-gcc7-opt', 'scriptenv': 'none', 'ncores': 2
'memory': 8589934592, 'spark-cluster': 'none' 
"""


import json
import requests
import subprocess
import os
import argparse
import sys
sys.path.append("..")
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from SessionUtils import Session
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import json
import time


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", dest="port", type=int,
                        required = True,
                        )
    parser.add_argument( "--users", nargs='+', dest="users",
                        required  = True,
                        help='list of users')
    parser.add_argument("--token", dest=" token",
                        required=True,
                        help = 'token value')

    parser.add_argument("--json", dest="json",
                         required=True,
                         help = 'json data')
    args = parser.parse_args()
    return args


class CreateSession:
    def __init__(self, port, users, token, params):
        self.port = port
        self.users = users
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.ref_test_name = "Session_creation_test"
        self.exit = 0
        self.token = token
        self.data = params
        self.ref_timestamp = int(time.time())
        self.session = Session(self.port, users, token, params)
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)




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

    def check_create_server(self):

        self.log.write("info", "creating servers..")
        for user in self.users:
            global r
            try:
                r = self.session.create_server(user)
            except requests.exceptions.RequestException as e:
                self.exit |= 1
                self.log.write("error", "status code " + str(r.status_code) + " " + str(e))

            else:
                if r.status_code == 202:
                    self.log.write("info", "Successfully requested the server")
                    """
                     After requesting a server it needs to respond within 30 seconds otherwise there will be 
                     Timeout Error
                     Example:
        
                     TimeoutError: Server at http://172.18.0.15:8888/user/user0/ didn't respond in 30 seconds
                     So, even after a successful request a server may not be created
                    """
                    time.sleep(30)

                    """
                    Try to create a same server again, a conflict request for creating a server returns  400 status code 
                    An example from log:
                    
                    [W 2019-06-29 14:46:20.850 SWAN web:1782] 400 POST /hub/api/users/user1/server (::ffff:127.0.0.1): user1 is already running
                    """
                    check_session = self.session.create_server(user)
                    if(check_session.status_code==400):
                        self.log.write("info", "Successfully created the" + user + " server")

                    else:
                        self.log.write("error",  user + " server was not created")
                        self.exit |= 1
                elif r.status_code == 201:
                    """
                    Sometimes servers are created without any wait time
                    """
                    self.log.write("info", "Successfully created the" + user + " server")

                else:
                    self.log.write("error", user + " server was not created")
                    self.log.write("error", "status code " + str(r.status_code) + " " + (r.content).decode('utf-8'))
                    self.exit |= 1

        return self.exit


    def exit_code(self):
        self.exit |= self.check_create_users()
        self.exit |= self.check_create_server()

        self.log.write("info", "overall exit code" + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    print(args.json)
    test_session = CreateSession(args.port, args.users, args.token, args.json)
    (test_session.exit_code())

