
import json
import requests
import subprocess
import os
import argparse
import sys
sys.path.append("..")
from SessionUtils import  JupyterhubTest
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
    parser.add_argument("--delay", dest="delay",
                        required=True,
                        help='delay while creating the server')

    parser.add_argument("--json", dest="json",
                         required=True,
                         help = 'json data')

    parser.add_argument("--token", dest = "token",
                        required= False,
                        help='token')

    parser.add_argument("--base_path", dest="base",
                        required=False,
                        help='base path')
    args = parser.parse_args()

    return args


class CreateSession(JupyterhubTest):
    """
    Create a session

    To run the test run the following command:

     python3 test_create_session.py --port 443 --users user3 --delay 30 --json '{"LCG-rel": "LCG_95a", "platform": "x86_64-centos7-gcc7-opt", "scriptenv": "none", "ncores": 2, "memory": 8589934592, "spark-cluster": "none"}'


    For multiple users

    python3 test_create_session.py --port 443 --users user0 user1 user2 --delay 30 --json '{"LCG-rel": "LCG_95a", "platform": "x86_64-centos7-gcc7-opt", "scriptenv": "none", "ncores": 2, "memory": 8589934592, "spark-cluster": "none"}'

    """
    def __init__(self, port, token, users, data, delay,  base_path, verify):
        param = {}
        param['test_name'] = 'Session_Creation_test'
        JupyterhubTest.__init__(self, port,  token, base_path, verify, **param)
        self.data = data
        self.users = users
        self.delay = delay


    def check_create_session(self):

        self.log.write("info", "creating servers..")
        r = ""
        for user in self.users:
            try:
                r = super().api_calls("post", user, data = self.data, endpoint ="/server")
            except requests.exceptions.RequestException as e:
                self.exit = 1
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
                    """
                    maximum delay should not be more than 30s
                    """
                    time.sleep(self.delay)

                    """
                    Submit a  get request to  https://localhost:443/hub/api/users/user1, this will return the information
                    of particular user in json format, check the value of the field 'server' if it is null, server is not active

                    Example:

                    json of user having active server-
                    {"kind": "user", "name": "user1", "admin": false, "groups": [], "server": "/user/user1/", "pending": null,
                    }

                    json of user have non-active server -
                    {"kind": "user", "name": "user3", "admin": false, "groups": [], "server": null, "pending": null}

                    """
                    
                    
                    r = super().api_calls("get", user, endpoint = "")
                    if (r.status_code == 200):
                        status = r.json()
                        #print(status)
                        server_status = status['server']
                        if(server_status!= None):
                            self.exit = 0
                            self.log.write("info", user + " server successfully created " + server_status)
                        else:
                            self.log.write("error", user + " server was not created ")
                            self.log.write("error", "status code " + str(r.status_code) + " " + (r.content).decode('utf-8'))
                            self.exit |= 1
                elif r.status_code == 201:
                    """
                    Sometimes servers are created without any wait time
                    """
                    self.log.write("info", "Successfully created the" + user + " server")
                    self.exit =0

                else:
                    self.log.write("error", user + " server was not created")
                    self.log.write("error", "status code " + str(r.status_code) + " " + (r.content).decode('utf-8'))
                    self.exit |= 1

        return self.exit


    def exit_code(self):
        self.exit |= self.check_create_session()

        self.log.write("info", "overall exit code" + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    params = json.loads(args.json)
    test_session = CreateSession(args.port, args.token, args.users, params, int(args.delay), args.base, verify =False)
    (test_session.exit_code())

