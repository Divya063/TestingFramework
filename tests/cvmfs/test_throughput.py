"""
Run using the command:
python3 test_throughput.py --num 2 --repo_path cvmfs/sft.cern.ch --path cvmfs/sft.cern.ch/lcg/releases/

Benchmark performance when reading from the repository and compute the read throughput.

"""
import os
import argparse
import time
import subprocess
from TestBase import Test


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


class Throughput(Test):
    def __init__(self, num, repoPath, filePath):
        self.number = num
        self.repo_path = repoPath
        self.path = filePath
        self.ref_test_name = "Throughput"
        self.repo_path = os.path.join('/', repoPath)
        self.path = os.path.join('/', filePath)
        super().__init__()


    def run_test(self):
        exit_code = 0
        self.log.write("performance", "\t".join(
            ["file_name","time_connect", "time_starttransfer" " total_time"]), val="read")
        count_files = 0
        contain_files = 0
        for subdir, dirs, files in os.walk(self.path):
            count_files = count_files + 1
            for file in files:
                relevant_files = os.path.join(subdir, file)
                # checks if there is any file to read
                contain_files = contain_files + 1
                command = "curl -o /dev/null -s -w '%{time_connect} : %{time_starttransfer} : %{time_total}\n'" + " file:///" + relevant_files
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                if p.returncode == 0:
                    self.log.write("info", relevant_files + " " + (out).decode('utf-8'), val="read")
                else:
                    self.log.write("error", str(err, 'utf-8'))
                    exit_code = 1
            if count_files == self.number:
                break
        if contain_files == 0:
            exit_code = 1
        self.log.write("info", "overall exit code" + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_throughput = Throughput(args.num_packages, args.repo_path, args.path)
    test_throughput.run_test()




