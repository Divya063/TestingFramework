import os
import time
import sys

LOG_FOLDER = "logs"
LOG_EXTENSION = ".log"
LOG_DELIMITER = "| "


class Logger():
    def __init__(self, fname, output_mode):
        self.terminal = sys.stdout
        self.output_mode = output_mode
        self.fopen_success = None
        # types of messages for logging
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
        if output_mode:
            if not os.path.exists(log_folder):
                try:
                    os.makedirs(log_folder)
                except PermissionError:
                    self.terminal.write("[Logging] " + "Permission denied, cannot create directory" + "\n")
            self.fname = fname
            self.fopen_success = 0
            try:
                self.fout = open(fname, 'w')
            except PermissionError:
                self.fopen_success = 1
                self.terminal.write("[Logging] " + "Permission denied" + "\n")

    def write(self, msg_type, msg, val=None):
        try:
            type = self.msg_type[msg_type]
        except KeyError:
            type = "[None] "

        message = type + "%.4f" % time.time() + LOG_DELIMITER + msg + "\n"
        if val:
            message = type + "%.4f" % time.time() + " " + val + LOG_DELIMITER + msg + "\n"
        self.terminal.write(message)
        if self.fopen_success != 1 and self.output_mode:
            self.fout.write(message)
            self.fout.flush()
        self.terminal.flush()

    def close(self):
        self.fout.close()
