import os
import subprocess
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import yaml
import sys

sys.path.append("..")
from TestBase import Test

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class JupyterhubTest(Test):
    """Implements everything required to call Jupyterhub API """

    def __init__(self, hostname, port, token, base_path, verify, **kwargs):
        super().__init__(**kwargs)
        self.token = token
        self.port = port
        self.verify = verify
        self.hostname = hostname
        self.base_path = base_path

    def check_container(self, user):
        """Checks if a container is running"""

        s = subprocess.check_output('docker ps', shell=True)
        container_name = "jupyter-" + user
        if s.decode("utf-8").find(container_name) == -1:
            self.log.write("error", "Container is not running")
            return 1
        return 0

    def call_api(self, method, user=None, data=None, endpoint=""):
        url = "https://%s:%s" % (self.hostname, str(self.port))
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
