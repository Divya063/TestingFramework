import threading
import subprocess
import time
import sys
sys.path.append("..")
import _thread as thread
import os
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from test_main import Test
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--timeout", dest="timeout", type=int,
                        required=True,
                        help = 'Timeout for the function')
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
    def __init__(self, timeout, mount_points):
        self.mount_points = mount_points
        self.timeout = timeout
        params = {}
        params['test_name'] = "mount_sanity"
        Test.__init__(self, **params)


    def quit_function(self, fn_name):
        self.log.write("error", '{0} took too long'.format(fn_name))
        self.exit = 1
        sys.stderr.flush()  # Python 3 stderr is likely buffered.
        thread.interrupt_main()  # raises KeyboardInterrupt if function is taking too long

    def check_mount(self, timeout):
        self.log.write("info", "timeout set to " + str(timeout))
        """
        exit process if this function takes longer than "timeout" seconds
        """
        # will call the quit function, if execution is not completed within stipulated time frame
        timer = threading.Timer(timeout, self.quit_function, args=['check_mount'])
        timer.start()
        old = os.getcwd()
        for points in self.mount_points:
            try:
                os.chdir('/')
                #time.sleep(8)
                output = subprocess.check_output(
                    ['ls', '-l', '/eos/' + points], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as exc:
                self.exit = 1
                os.chdir(old)
                self.log.write("parameters", "Test name: " + self.ref_test_name)
                return
            finally:
                timer.cancel()
                os.chdir(old)
            self.log.write("info", "mount point "+ points +" tested")
            self.exit =0

    def exit_code(self):
        self.exit = self.check_mount(self.timeout)
        self.log("overall exit code " + str(self.exit))
        return self.exit

if __name__ == "__main__":
    args = get_args()
    test_mount_sanity = MountSanity(args.timeout, args.mount_points)
    test_mount_sanity.exit_code()

