import time
import os
import sys

sys.path.append("..")
import yaml
import pickle
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from grafana import Grafana


class Test:
    """Output Configuration"""

    def __init__(self, yaml_path=None, **kwargs):
        # for storing statistics
        self.stats = {}
        self.params = kwargs
        if yaml_path:
            tasks = self.load_conf(yaml_path)
        else:
            tasks = self.load_pickle()
        self.stats[self.ref_test_name] = Grafana()
        self.to_logs = tasks['output']['logfile']['logging']
        self.grafana = tasks['output']['grafana']
        self.to_grafana = self.grafana['push']
        self.module = self.grafana['modules']
        self.host = self.grafana['hostname']
        self.port = self.grafana['port']
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.ref_timestamp = int(time.time())
        self.log = Logger(os.path.join(self.logger_folder,
                                       self.ref_test_name + "_" + time.strftime("%Y-%m-%d_%H:%M:%S") + LOG_EXTENSION),
                          self.to_logs)
        if self.to_logs:
            self.log_params()

    # if you are running the tests individually, this will be needed to pass the output configuration
    # TODO Two things can be done here Take the yaml path from the user while running the tests individually, example
    #  -  python3 test_throughput.py --num 10 --file_size 1M --dest / --path /home/divya/TestingFramework/test.yaml
    #  Or take the output conf in dictionary format from the user (Currently following the first approach)

    def load_conf(self, path):
        with open(path, 'r') as stream:
            return yaml.safe_load(stream)

    # if you are using the main script (run.py) to run the tests
    # the output configuration has been stored inside a pickle file

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
        name = type(classname).__name__
        if name in self.module:
            Grafana.make_stats_and_publish(self, classname, self.host, self.port, self.to_grafana)
