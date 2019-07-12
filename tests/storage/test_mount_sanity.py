import threading
import subprocess
import time
import sys
import _thread as thread
import os
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--timeout", dest="timeout", type=int,
                        required=True,
                        help = 'Timeout for the function')

    args = parser.parse_args()
    return args

class MountSanity:
    def __init__(self, timeout):
        self.exit = 0
        self.ref_timestamp = int(time.time())
        self.timeout = timeout
        self.ref_test_name = 'mount_sanity'
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log.write("info", self.ref_test_name + " Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Logger folder: " + self.logger_folder)

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
        try:
            os.chdir('/')
            #time.sleep(8)
            output = subprocess.check_output(
                ['ls', '-l', '/eos/'], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            self.exit = 1
            os.chdir(old)
            self.log.write("parameters", "Test name: " + self.ref_test_name)
            return
        finally:
            timer.cancel()
            os.chdir(old)
        self.log.write("info", "command successfully executed")

    def exit_code(self):
        self.exit = self.check_mount(self.timeout)
        return self.exit

if __name__ == "__main__":
    args = get_args()
    test_mount_sanity = MountSanity(args.timeout)
    test_mount_sanity.exit_code()

