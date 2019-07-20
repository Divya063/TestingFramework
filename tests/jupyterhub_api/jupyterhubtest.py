import os
import subprocess
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import yaml
import sys

sys.path.append("..")
from Test import Test

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class JupyterhubTest(Test):
    """Implements everything required to call Jupyterhub API """

    def __init__(self, port, token, base_path, verify):
        Test.__init__(self)
        self.token = token
        self.port = port
        self.verify = verify
        self.base_path = base_path

    def call_api(self, method, user=None, data=None, endpoint=""):
        url = "https://localhost:" + str(self.port)
        api_url = url + ("/%s" % self.base_path if self.base_path else "") + "/hub/api/"

        if user:
            api_url = api_url + 'users/%s' % user + endpoint

        request = requests.session()
        request.verify = False

        try:
            headers = {
                'Authorization': 'token %s' % self.token,
            }

            method_function = getattr(request, method)

        except AttributeError:
            raise Exception

        else:
            response = method_function(api_url, headers=headers, json=data)
            return response
