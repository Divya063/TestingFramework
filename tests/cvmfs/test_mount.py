import os
import argparse
import subprocess
import time
from tests.logger import Logger, LOG_FOLDER, LOG_EXTENSION


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
    def __init__(self, repo_name, repo_path):
        self.repo_name = repo_name
        self.repo_path = repo_path
        self.ref_test_name = "cvmfs_mount"
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name + LOG_EXTENSION))
        self.log.write("info", "Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.exit = None
        self.ref_timestamp = int(time.time())
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))


    def check_empty(self, repo_path):
        if(next(os.scandir(repo_path), None) is None):
            self.log.write("error", repo_path + " is empty")
            self.exit|=1



    def check_mount(self, repo_path):
        first_command = subprocess.Popen(["mount", "-l"], stdout=subprocess.PIPE)
        second_command = subprocess.Popen(["grep", repo_path], stdin=first_command.stdout)
        if(second_command):
            self.log.write("sanity", repo_path + " exists")
            self.exit = 0
            self.check_empty(repo_path)
        else:
            self.log.write("error", repo_path + " does not exists")
            self.exit = 1
        return self.exit

    def exit_code(self):
        code = self.check_mount(self.repo_path)
        self.log.write("info", "exit code: " + str(self.exit))
        return code


if __name__ == "__main__":
    args = get_args()
    test_mount = Mount(args.repo_name, args.path)
    test_mount.exit_code()









