import threading
import subprocess
import time
import sys
sys.path.append("..")
import _thread as thread
import os
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from Test import Test
import argparse

class Mount(Test):
    """
    Checks for eos mount points
    """
    def __init__(self):
        self.ref_test_name = "mount"
        Test.__init__(self)


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

