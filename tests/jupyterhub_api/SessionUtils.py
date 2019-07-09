import os
import subprocess
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import yaml
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Session:

    def __init__(self, port, users, path, params, verify):
        self.port = port
        self.users = users
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.exit = 0
        self.path = path
        self.token = ""
        self.data = params
        self.verify = verify


    def create_load_token(self):
        owd = os.getcwd()
        os.chdir(os.path.expanduser(self.path))
        command = subprocess.check_output(["jupyterhub", "token", "dummy_admin"], stderr=subprocess.STDOUT) \
            .decode('utf-8').split(
            '\n')
        size = len(command)

        self.token = command[size - 2]
        os.chdir(owd)
        print("token is  " + self.token)
        """
        get back to old directory
        """

        path = os.path.join('/', 'test.yaml')
        print(path)
        if os.path.exists(path):
            with open(path) as f:
                tasks = yaml.safe_load(f)

            test_jupyterhub = tasks['tests']['jupyterhub_api']
            test_jupyterhub['create_session']['token'] = self.token
            try:
                with open(path, 'w') as file:
                    yaml.dump(tasks, file, default_flow_style=False)
            except Exception as e:
                raise Exception

            #print(test_jupyterhub['create_session']['token'])


        else:
            raise Exception("yaml file not present")
            sys.exit()
        return self.token, command


    def create_server(self, user):


        r = requests.post(self.main_url + 'users/%s' % user + "/server",
                          headers={
                              'Authorization': 'token %s' % self.token,
                          },
                          json=self.data,
                          verify= self.verify
                          )
        return r

