import hashlib
import os
import glob
import traceback
import re
import binascii
import logging
import sys

sys.path.append("..")
import time
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
import argparse
from TestBase import Test
from pathlib import Path


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dest", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args


class Exists(Test):
    """Check whether a given file exists or not (in the given path)"""

    def __init__(self, filePath):
        self.file_path = filePath
        self.ref_test_name = "file_exists"
        self.params = {}
        self.params['file_path'] = self.file_path
        super().__init__(**self.params)

    def run_test(self):
        self.log.write("info", "Start of search operation")
        exit_code = 0
        try:
            file = Path(self.file_path)
            if file.is_file():
                self.log.write("info", "File " + self.file_path + " detected", val="search")
                self.log.write("info", "exit code: " + str(exit_code))
            else:
                self.log.write("error", "File " + self.file_path + " not detected", val="search")
                exit_code = 1
        except Exception as e:
            self.log.write("error", str(e))
            exit_code = 1

        self.log.write("info", "overall exit code " + str(exit_code))
        return exit_code



if __name__ == "__main__":
    args = get_args()
    test_exists = Exists(args.path)
    test_exists.run_test()
