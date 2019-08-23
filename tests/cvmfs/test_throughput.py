"""
Run using the command:
python3 test_throughput.py --num 2 --repo_path cvmfs/sft.cern.ch --path cvmfs/sft.cern.ch/lcg/releases/

Benchmark performance when reading from the repository and compute the read throughput.

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
    def __init__(self, num, repoPath, filePath):
        self.number = num
        self.repo_path = repoPath
        self.path = filePath
        self.ref_test_name = "Throughput"
        self.repo_path = os.path.join('/', repoPath)
        self.path = os.path.join('/', filePath)
        self.mount = Mount(repoPath, filePath)
        self.ref_timestamp = int(time.time())
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log.write("info", "Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))

    def run_test(self, num_packages, repo_path, path):
        exit_code = 0
        if (self.mount.check_mount(repo_path) == 0):
            self.log.write("performance", "\t".join(
                ["file_name","time_connect", "time_starttransfer" " total_time"]), val="read")
            count = 0
            for subdir, dirs, files in os.walk(path):
                count = count + 1
                for file in files:
                    relevant_files = os.path.join(subdir, file)
                    print(relevant_files)

                    command = "curl -o /dev/null -s -w '%{time_connect} : %{time_starttransfer} : %{time_total}\n'" + " file:///" + relevant_files
                    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    out, err = p.communicate()
                    if (p.returncode ==0):
                        self.log.write("info", relevant_files + " " + (out).decode('utf-8'), val ="read")
                    else:
                        self.log.write("error", str(err, 'utf-8'))
                        exit_code = 1
                if count == num_packages:
                    break
        else:
            self.log.write("error", "repository is not mounted")
            exit_code = 1

        self.log.write("info", "overall exit code" + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_throughput = Throughput(args.num_packages, args.repo_path, args.path)
    test_throughput.run_test()




