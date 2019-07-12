"""
Test if a session is running

To run the test use the following command:
python3 test_check_session.py --port 443 --users user1

For multiple users

python3 test_check_session.py --port 443 --users user0 user1 user2

"""

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
from SessionUtils import Session
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
    args = parser.parse_args()
    return args


class CheckSession:
    def __init__(self, port, users, verify):
        self.users = users
        self.port = port
        self.exit =0
        self.verify = verify
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.ref_test_name= "Check_Sessions"
        self.ref_timestamp = int(time.time())
        self.session = Session()
        self.token = self.session.get_tokens()
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)


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

            third method:
            Submit a  get request to  https://localhost:443/hub/api/users/user1, this will return the information
            of particular user in json format, check the value of the field 'server' if it is null server is not active

            Example:
                json of user having active server-
                {"kind": "user", "name": "user1", "admin": false, "groups": [], "server": "/user/user1/", "pending": null,
                }

                json of user have non-active server -
                {"kind": "user", "name": "user3", "admin": false, "groups": [], "server": null, "pending": null}



            """
            global r
            #self.token = '787fc9a32e1d477daa2be4202031bb28'
            for user in self.users:
                try:
                    r = requests.get(self.main_url + 'users/%s' % user,
                                        headers={
                                            'Authorization': 'token %s' % self.token,
                                        },
                                        verify= self.verify
                                        )

                except requests.exceptions.RequestException as e:
                    self.log.write("error", str(e))
                    self.exit |= 1
                else:
                    if (r.status_code == 200):
                        status = r.json()
                        server_status = status['server']
                        if(server_status!= None):
                            self.log.write("info", user + " server is present at " + server_status)
                        else:
                            self.log.write("error", user + " server is not present ")
                            self.exit |= 1
                    else:
                        self.log.write("error", (r.content).decode('utf-8'))
                        self.exit |= 1

            return self.exit



    def exit_code(self):
        self.exit |= self.check_session()

        return self.exit

if __name__ == "__main__":
    args = get_args()
    test_active_session = CheckSession(args.port, args.users, verify=False)
    (test_active_session.exit_code())


