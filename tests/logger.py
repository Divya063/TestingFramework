import os
import time

LOG_FOLDER      = "logs"
LOG_EXTENSION   = ".log"
LOG_DELIMITER   = "| "

class Logger():
    def __init__(self, fname):
        #types of messages for logging
        self.msg_type = {
            "parameters": "[PARAMS] ",
            "info": "[INFO] ",
            "performance": "[PERF] ",
            "consistency": "[INTEGRITY] ",
            "warning": "[WARNING] ",
            "error": "[ERROR] ",
        }

        # Make sure the output folder for logs is there
        log_folder = os.path.split(fname)[0]
        if (not os.path.exists(log_folder)):
            os.makedirs(log_folder)
        self.fname = fname
        self.fout = open(fname, 'w')

    def write(self, msg_type, msg, val=None):
        try:
            type = self.msg_type[msg_type]
        except KeyError:
            type = "[None] "

        message = type + "%.4f" % time.time() + LOG_DELIMITER + msg + "\n"
        if (val!=None):
            message = type + "%.4f" % time.time() + " " + val + LOG_DELIMITER + msg + "\n"
        self.fout.write(message)
        self.fout.flush()

    def close(self):
        self.fout.close()
