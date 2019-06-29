"""
Test if a session is running
"""

import json
import requests
import subprocess
import os
import docker

import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( "--users", nargs='+', dest="users",
                        required  = True,
                        help='list of users')
    parser.add_argument("--port", dest="port", type=int,
                        required=True,
                        )
    args = parser.parse_args()
    return args


class CheckSession:
    def __init__(self, users, port):
        self.user = users
        self.port = port
        self.exit =0
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"


    def check_session(self):
        s = subprocess.check_output('docker ps', shell=True)
        sessions_not_running = set()
        for user in self.user:
            container_name = "jupyter-" + user
            """
            check if user container is up and running
            """
            if(s.decode("utf-8").find(container_name) == -1):
                sessions_not_running.add(user)
                self.exit|=1
            """
            Server at http://172.18.0.16:8888/user/{name}/ should respond with 302, 
            but if multiple servers are there only one of them would respond with 302
            Example :
            
            main_url = 'http://172.18.0.16:8888/'
            r = requests.get(main_url + 'user/%s' % user + '/',
                              )
            print(r.status_code)
            if r.status_code == 302:
                print("successful")
            """
            """
            Submit a post request to /hub/api/users/user2/server which will in return 
            result in 409 status code(conflict)
            """
            data = { "LCG-rel":"LCG_95a", "platform": "x86_64-centos7-gcc7-opt", "scriptenv": "none", "ncores": 2, "memory": 8589934592, "spark-cluster": "none"}

            r = requests.post(self.main_url + 'user/%s' % user + '/server', json = data, verify= False
                              )
            print(r.status_code)
            if r.status_code == 409:
                print("Session Exists")
            else:
                self.exit |= 1
                sessions_not_running.add(user)
                r.raise_for_status()

        return self.exit

    def exit_code(self):
        self.exit |= self.check_session()

        return self.exit

if __name__ == "__main__":
    args = get_args()
    test_check_session = CheckSession(args.users, args.port)
    print(test_check_session.exit_code())








