import os
import subprocess
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import yaml
import sys
sys.path.append("..")
from test_main import Test
import time
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class JupyterhubTest(Test):
    """

    Implements everything required to call Jupyterhub API
    """

    def __init__(self, port, token, base_path, verify, **kwargs):
        Test.__init__(self, **kwargs)
        self.exit = 0
        self.token = token
        self.port = port
        self.verify = verify
        self.base_path = base_path


    def api_calls(self, method,user, data = None,  endpoint=""):
        url = "https://localhost:" + str(self.port)
        if (self.base_path != None):
            main_url = url + "/" + self.base_path + "/hub/api/"
        else:
            main_url = url + "/hub/api/"

        if user!="":
            api_url = main_url + 'users/%s' %user + endpoint
        else:
            api_url = main_url

        request = requests.session()
        request.verify = False

        r = ""
        try:
            headers = {
                'Authorization': 'token %s' % self.token,
            }
            if(method == "post"):
                r = request.post(api_url, headers = headers, json = data)

            elif(method == "get"):
                r = request.get(api_url, headers = headers)

            elif(method == "delete"):
                r = request.delete(api_url, headers= headers)


        except requests.exceptions.RequestException:
            r.raise_for_status()

        else:
            return r





