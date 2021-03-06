import threading
import subprocess
import time
import sys

sys.path.append("..")
import _thread as thread
import os
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from TestBase import Test
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--timeout", dest="timeout", type=int,
                        required=True,
                        help='Timeout for the function')
    parser.add_argument("--mount_points", nargs='+', dest="mount_points", type=str,
                        required=True,
                        help='Mount Points')
    args = parser.parse_args()
    return args


class MountSanity(Test):
    """
    Checks Sanity of mount points

    Command - python3 test_mount_sanity.py --timeout 5 --mount_points user user/u

    """

    def __init__(self, timeout, mountpoints):
        self.mount_points = mountpoints
        self.timeout = timeout
        self.ref_test_name = "mount_sanity"
        # self.exit is needed in both the functions (quit_function and run_test)
        self.exit = 0
        super().__init__()

    def quit_function(self, fn_name):
        self.log.write("error", '{0} took too long'.format(fn_name))
        self.exit = 1
        thread.exit()

    def run_test(self):
        self.log.write("info", "timeout set to " + str(self.timeout))

        # exit process if this function takes longer than "timeout" seconds

        # will call the quit function, if execution is not completed within stipulated time frame
        timer = threading.Timer(self.timeout, self.quit_function, args=['check_mount'])
        timer.start()
        old = os.getcwd()
        for point in self.mount_points:
            try:
                os.chdir('/')
                output = subprocess.check_output(
                    ['ls', '-l', 'eos/' + point], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as exc:
                os.chdir(old)
                self.log.write("error", str(exc))
                self.exit = 1
                return self.exit
            finally:
                timer.cancel()
                os.chdir(old)
            self.log.write("info", "mount point " + point + " tested")
        self.log.write("info", "exit code " + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_mount_sanity = MountSanity(args.timeout, args.mount_points)
    test_mount_sanity.run_test()
