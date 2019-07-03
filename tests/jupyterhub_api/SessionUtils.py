import os
import subprocess
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Session:

    def __init__(self, port, users, token, params):
        self.port = port
        self.users = users
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.exit = 0
        self.token = token
        self.data = params

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


        r = requests.post(self.main_url + 'users/%s' % user + "/server",
                          headers={
                              'Authorization': 'token %s' % self.token,
                          },
                          json=self.data,
                          verify=False
                          )
        return r

