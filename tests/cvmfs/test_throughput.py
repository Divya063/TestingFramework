"""
Run using the command:
python3 test_throughput.py --num 5 --repo_path cvmfs/sft.cern.ch --path cvmfs/sft.cern.ch/lcg/releases/
"""
import os
import argparse
import time
import subprocess

from test_mount import Mount
from logger import Logger, LOG_FOLDER, LOG_EXTENSION


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--num", dest="num_packages",
                        required=True,
                        help='Number of packages')
    parser.add_argument("--repo_path", dest="repo_path",
                        required=True,
                        help='Specify the repository path')

    parser.add_argument("--path", dest="path",
                        help='Specify the path')

    args = parser.parse_args()
    return args

class Throughput:
    def __init__(self, num_packages, repo_path, path):
        self.number = num_packages
        self.repo_path = repo_path
        self.path = path
        self.ref_test_name = "Throughput"
        self.exit = 0
        self.parent = os.path.join(os.getcwd(), os.pardir)
        self.repo_path = os.path.join(self.parent, repo_path)
        self.path = os.path.join(self.parent, path)
        self.mount = Mount(repo_path, path)
        #print(repo_path)
        self.ref_timestamp = int(time.time())
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name + LOG_EXTENSION))
        self.log.write("info", "Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))


    def read(self, num_packages, repo_path, path):
        if (self.mount.check_mount(repo_path) == 0):
            count = 0
            for subdir, dirs, files in os.walk(path):
                count = count +1
                for file in files:
                    relevant_files = os.path.join(subdir, file)

                    command = "curl -o /dev/null -s -w 'Total: %{time_total}s\n'" + " file:///" + relevant_files
                    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = p.communicate()
                    if (str(err, 'utf-8')) == "":
                        self.log.write("info", "time taken " + str(out))
                    else:
                        self.log.write("error", str(err, 'utf-8'))
                        self.exit |= 1
                if(count == num_packages):
                    break
        else:
            self.log.write("error", "repository is not mounted")
            self.exit |= 1

        return self.exit

    def exit_code(self):
        code = self.read(self.number, self.repo_path, self.path)
        self.log.write("info", "exit code: " + str(self.exit))
        return code



if __name__ == "__main__":
    args = get_args()
    test_throughput = Throughput(args.num_packages, args.repo_path, args.path)
    test_throughput.exit_code()




