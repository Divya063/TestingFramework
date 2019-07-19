import os
import time
from logger import Logger, LOG_FOLDER, LOG_EXTENSION

class Test:
    """
    Implements logs
    """
    def __init__(self, **kwargs):
        self.ref_test_name = kwargs.get('test_name')
        self.kwargs = kwargs
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.ref_timestamp = int(time.time())
        self.log = Logger(os.path.join(self.logger_folder,
                                       self.ref_test_name + "_" + time.strftime("%Y-%m-%d_%H:%M:%S") + LOG_EXTENSION))
        self.log.write("info", time.strftime("%c"))
        self.log.write("info", self.ref_test_name + " Tests starting...")
        self.log_params()


    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)
        for key, value in self.kwargs.items():
            self.log.write("parameters", "%s : %s" % (key, value))