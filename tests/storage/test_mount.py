import threading
import subprocess
import time
import sys
import _thread as thread
import os
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
import argparse

class Mount:
    def __init__(self):
        self.exit = 0
        self.ref_timestamp = int(time.time())
        self.ref_test_name = 'mount'
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log.write("info", self.ref_test_name + " Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)



    def check_mount(self):
        olddir = os.getcwd()
        os.chdir('/')
        first_command = subprocess.Popen(["mount", "-l"], stdout=subprocess.PIPE)
        second_command = subprocess.Popen(["grep", "eos"], stdin=first_command.stdout)
        if (second_command):
            self.log.write("sanity", "eos mount points" + " exist")
            self.exit = 0
        else:
            self.log.write("error", "eos mount points" + " do not exist")
            self.exit = 1
        return self.exit


    def exit_code(self):
        self.exit = self.check_mount()
        return self.exit

if __name__ == "__main__":
    test_mount = Mount()
    test_mount.exit_code()

