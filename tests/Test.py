
import time
import os
import sys
sys.path.append("..")
import pickle
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from grafana import Grafana

class Test:
    """Output Configuration"""

    params = {}

    def __init__(self, to_logs=None, to_grafana=None):
        # for storing statistics
        self.stats = {}
        tasks = self.load_pickle()
        self.stats[self.fname] = Grafana()
        self.to_logs = tasks['output']['logfile']['to_logs']
        self.grafana = tasks['output']['grafana']
        self.to_grafana = self.grafana['to_grafana']
        self.module = self.grafana['modules']
        self.host = self.grafana['hostname']
        self.port = self.grafana['port']
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.ref_timestamp = int(time.time())
        self.log = Logger(os.path.join(self.logger_folder,
                                       self.ref_test_name + "_" + time.strftime("%Y-%m-%d_%H:%M:%S") + LOG_EXTENSION), self.to_logs)
        if self.to_logs:
            self.log_params()

    def load_pickle(self):
        with open('tests/tasks.pkl', 'rb') as f:
            tasks = pickle.load(f)
        return tasks


    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)
        for key, value in self.params.items():
            self.log.write("parameters", "Param %s has value %s" % (key, value))

    def check_test_class(self, classname):
        if classname in self.module:
            Grafana.make_stats_and_publish(self, classname, self.host, self.port, self.to_grafana)


