"""

Evaluates the time needed to get the first byte (TTFB) of a file known to exist.

Run using the command:
python3 test_ttfb.py ---repo sft.cern.ch --path cvmfs/sft.cern.ch/lcg/lastUpdate

"""
import argparse
import os
import time
import sys
sys.path.append('..')
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from test_mount import Mount

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--repo", dest="repo_name",
                        required=True,
                        help='Repository name')

    parser.add_argument("--path", dest="file_path",
                        required=True,
                        help='Specify the path (file included)')

    args = parser.parse_args()
    return args

class Ttfb:
    def __init__(self, repo_path, path):
        self.exit = None
        #self.parent = os.path.join(os.getcwd(), os.pardir)
        self.repo_path = os.path.join('/', repo_path)
        self.path = os.path.join('/', path)
        print(repo_path)
        self.mount = Mount(repo_path, path)
        self.ref_test_name = "Time_till_First_Byte"
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log.write("info", "Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.exit = 0
        self.ref_timestamp = int(time.time())
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))


    def ttfb(self, repo_path, path):
        global ttfb
        if(self.mount.check_mount(repo_path) == 0):
            start = time.time()
            try:
                with open(path, 'rb') as file:
                    # read one byte
                    file.read(1)
                    ttfb = time.time() - start
            except Exception as err:
                self.log.write("error", "Error while reading " + path)
                self.log.write("error", path + ": " + str(err))
                self.exit |= 1

            else:
                self.log.write("Performance", "\t".join(
                    [path,  str(("%.8f" % float(ttfb)))]))
        else:
            self.log.write("error", "repository is not mounted")
            self.exit |= 1

        return self.exit

    def exit_code(self):
        code = self.ttfb(self.repo_path, self.path)
        self.log.write("info", "exit code: " + str(self.exit))
        return code

if __name__ == "__main__":
    args = get_args()
    test_ttfb = Ttfb(args.repo_name, args.path)
    test_ttfb.exit_code()