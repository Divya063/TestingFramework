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
from TestBase import Test


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--repo", dest="repo_name",
                        required=True,
                        help='Repository name')

    parser.add_argument("--path", dest="file_path",
                        required=True,
                        help='Specify the path (file included)')

    args = parser.parse_args()
    return args


class Ttfb(Test):
    def __init__(self, repoPath, filePath):
        self.repo_path = os.path.join('/', repoPath)
        self.path = os.path.join('/', filePath)
        self.ref_test_name = "Time_till_First_Byte"
        super().__init__()

    def run_test(self):
        ttfb = 0
        exit_code = 0

        start = time.time()
        try:
            with open(self.path, 'rb') as file:
                # read one byte
                file.read(1)
                ttfb = time.time() - start
        except Exception as err:
            self.log.write("error", "Error while reading " + self.path)
            self.log.write("error", self.path + ": " + str(err))
            exit_code = 1

        else:
            self.log.write("Performance", "\t".join(
                [self.path, str(("%.8f" % float(ttfb)))]))

        self.log.write("info", "exit code: " + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_ttfb = Ttfb(args.repo_name, args.path)
    test_ttfb.run_test()
