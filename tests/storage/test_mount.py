import threading
import subprocess
import time
import sys

sys.path.append("..")
import _thread as thread
import os
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from TestBase import Test
import re
import urllib
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--mode", dest="mode",
                        required=True,
                        help='Specify the mode (e.g, 0 - host mode, 1 - sciencebox ')
    args = parser.parse_args()
    return args


class Mount(Test):
    """Checks for eos mount points"""

    def __init__(self, mode):
        self.ref_test_name = "mount"
        self.mode = mode
        super().__init__()

    def check_mount(self):
        olddir = os.getcwd()
        os.chdir('/')
        first_command = subprocess.Popen(["mount", "-l"], stdout=subprocess.PIPE)
        out, err = first_command.communicate()
        regex = re.compile(r'\b(eos.*on.*type.*fuse.*)\b', re.MULTILINE)
        regex_second = re.compile(r'\b(home-.*on*type.fuse.*)\b', re.MULTILINE)
        regex_docker_mount = re.compile(r'\b(eosdocker.*on.*/eos/.*type.*fuse)\b', re.MULTILINE)

        # On sciencebox , mount -l | grep eos resulted in
        # /dev/sda5 on /tmp/sciencebox/eos_mount type ext4 (rw,relatime,errors=remount-ro,stripe=32699,data=ordered)

        regex_docker_mount_second = re.compile(r'\b(.*/tmp/sciencebox/eos_mount.*type.*)\b', re.MULTILINE)
        out = out.decode('utf-8')
        result = regex.findall(out)
        result_host = regex_second.findall(out)
        result_docker = regex_docker_mount.findall(out)
        result_docker_second = regex_docker_mount_second.findall(out)

        # Two testing modes are there: host, sciencebox, if eos is mounted on host as well as on sciencebox
        # exit code will be zero, in case if mode is sciencebox and eos is mounted only on host, exit
        # code will be 1
        exit_code_host = 1
        exit_code_container = 1
        exit_code = 0
        if result and result_host:
            self.log.write("sanity", "eos mount points exist on host")
            exit_code_host = 0
        if result_docker or result_docker_second:
            self.log.write("sanity", "[sciencebox] eos mount points exist")
            exit_code_container = 0

        if exit_code_container and self.mode == "sciencebox":
            exit_code = 1
            self.log.write("sanity", "eos mount points do not exist on sciencebox")
        elif exit_code_host and self.mode == "host":
            self.log.write("sanity", "eos mount points do not exist on host")
            exit_code = 1

        os.chdir(olddir)

        if exit_code:
            return 1
        return 0

    def exit_code(self):
        self.exit = self.check_mount()
        self.log.write("info", "overall exit code " + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_mount = Mount(args.mode)
    test_mount.exit_code()
