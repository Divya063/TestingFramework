import os
import subprocess
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import yaml
import time
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from logger import Logger, LOG_FOLDER, LOG_EXTENSION


class Test:
    """
    Implements logs
    """
    def __init__(self):
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.ref_test_name = ""
        self.ref_timestamp = int(time.time())
        self.log = Logger(os.path.join(self.logger_folder,
                                       self.ref_test_name + "_" + time.strftime("%Y-%m-%d_%H:%M:%S") + LOG_EXTENSION))


    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)

class JupyterhubTest(Test):
    """

    Implements everything required to call Jupyterhub API
    """

    def __init__(self, port, base_path, verify):
        Test.__init__(self)
        self.exit = 0
        self.token = ""
        self.port = port
        self.verify = verify
        self.base_path = base_path
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


    def api_calls(self, method,user, data = None,  endpoint=""):
        if (self.base_path != None):
            main_url = "https://localhost:" + str(self.port) + "/" + self.base_path + "/hub/api/"
        else:
            main_url = "https://localhost:" + str(self.port) + "/hub/api/"

        if user!="":
            api_url = main_url + 'users/%s' %user + endpoint
        else:
            api_url = main_url
        print(api_url)
        r = ""
        try:
            if(method == "post"):
                r = requests.post(api_url,
                                  headers={
                                      'Authorization': 'token %s' % self.token,
                                  },
                                  json= data,
                                  verify=self.verify
                                  )
            elif(method == "get"):
                r = requests.get(api_url,
                                  headers={
                                      'Authorization': 'token %s' % self.token,
                                  },
                                  verify=self.verify
                                  )
            elif(method == "delete"):
                r = requests.delete(api_url,
                                 headers={
                                     'Authorization': 'token %s' % self.token,
                                 },
                                 verify=self.verify
                                 )
        except requests.exceptions.RequestException:
            r.raise_for_status()

        else:
            return r





