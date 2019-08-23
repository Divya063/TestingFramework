"""
python3 test_mount.py --repo sft.cern.ch --path cvmfs/sft.cern.ch/
"""

import os
import argparse
import subprocess
import time
import sys

sys.path.append("..")
from TestBase import Test


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--repo", dest="repo_name",
                        required=True,
                        help='Repository name')

    parser.add_argument("--path", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args


class Mount(Test):
    def __init__(self, repoName, repoPath):
        self.repo_name = repoName
        self.repo_path = repoPath
        self.ref_test_name = "cvmfs_mount"
        self.repo_path = os.path.join('/', repoPath)
        self.params = {}
        self.params['repo_path'] = self.repo_path
        super().__init__(**self.params)

    def run_test(self):
        exit_code = 0
        first_command = subprocess.Popen(["mount", "-l"], stdout=subprocess.PIPE)
        second_command = subprocess.Popen(["grep", self.repo_path], stdin=first_command.stdout)
        if second_command:
            self.log.write("sanity", self.repo_path + " exists")
        else:
            self.log.write("error", self.repo_path + " does not exists")
            exit_code = 1

        self.log.write("info", "overall exit code" + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_mount = Mount(args.repo_name, args.path)
    test_mount.run_test()
