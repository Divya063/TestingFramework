"""
python3 test_mount.py --repo sft.cern.ch --path cvmfs/sft.cern.ch/
"""

import os
import argparse
import subprocess
import time
import sys
sys.path.append("..")
from logger import Logger, LOG_FOLDER, LOG_EXTENSION


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--repo", dest="repo_name",
                        required=True,
                        help='Repository name')

    parser.add_argument("--path", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args


class Mount:
    def __init__(self, repoName, repoPath):
        self.repo_name = repoName
        self.repo_path = repoPath
        self.ref_test_name = "cvmfs_mount"
        #self.parent= os.path.join(os.getcwd(), os.pardir)
        self.repo_path = os.path.join('/', repoPath)
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

    def run_test(self, repo_path):
        exit_code = 0
        first_command = subprocess.Popen(["mount", "-l"], stdout=subprocess.PIPE)
        second_command = subprocess.Popen(["grep", repo_path], stdin=first_command.stdout)
        if second_command:
            self.log.write("sanity", repo_path + " exists")
        else:
            self.log.write("error", repo_path + " does not exists")
            exit_code = 1

        self.log.write("info", "overall exit code" + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_mount = Mount(args.repo_name, args.path)
    test_mount.run_test()