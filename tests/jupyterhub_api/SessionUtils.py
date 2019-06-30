import os
import subprocess
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class CreateSession:

    def __init__(self, port, users, path):
        self.port = port
        self.users = users
        self.path = path
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.exit = 0
        self.token =0



    def create_token(self):
        owd = os.getpwd()
        os.chdir(os.path.expanduser(self.path))
        command = subprocess.check_output(["jupyterhub", "token", "dummy_admin"], stderr=subprocess.STDOUT)\
            .decode('utf-8').split(
            '\n')
        size = len(command)

        self.token = command[size-2]
        """
        get back to old directory
        """
        os.chdir(owd)
        return self.token, command

    def create_users(self, user):

        """
        Inside container
        port = 443

        Ouside container
        port = 8443
        """

        r = requests.post(self.main_url + 'users/%s' % user,
                          headers={
                              'Authorization': 'token %s' % self.token,
                          },
                          verify=False
                          )
        return r

    def create_server(self, user):
        data = {"LCG-rel": "LCG_95a", "platform": "x86_64-centos7-gcc7-opt", "scriptenv": "none", "ncores": 2,
                "memory": 8589934592, "spark-cluster": "none"}

        r = requests.post(self.main_url + 'users/%s' % user + "/server",
                          headers={
                              'Authorization': 'token %s' % self.token,
                          },
                          json=data,
                          verify=False
                          )
        return r

