import os
import subprocess
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import yaml
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Session:

    def __init__(self):
        self.exit = 0
        self.token = ""
        self.get_tokens()

    def get_tokens(self):
        """
        Get token from yaml file
        """
        path = os.path.join('/', 'test.yaml')
        # path = "/".join(script_directory) + "/" + 'test.yaml'
        if os.path.exists(path):
            with open(path) as f:
                tasks = yaml.safe_load(f)

            test_jupyterhub = tasks['tests']['jupyterhub_api']
            self.token = test_jupyterhub['create_session']['token']
        else:
            raise Exception

        return self.token

    def create_server(self, port, user, data, verify):
        main_url = "https://localhost:" + str(port) + "/hub/api/"


        r = requests.post(main_url + 'users/%s' % user + "/server",
                          headers={
                              'Authorization': 'token %s' % self.token,
                          },
                          json= data,
                          verify= verify
                          )
        return r




