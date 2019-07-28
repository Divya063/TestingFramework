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

extension = ".txt"


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--file_name", dest="file_name",
                        required=True,
                        help='Name of the file')
    parser.add_argument("--dest", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args


class Exists(Test):
    """Check whether a given file exists or not (in the given path)"""

    def __init__(self, file_name, dest_path):
        self.storage_path = dest_path
        self.file_name = file_name
        self.root_file_path = os.path.join("/", dest_path)
        self.file_path = os.path.join(self.root_file_path, file_name)
        self.ref_test_name = "file_exists"
        self.params = {}
        self.params['file_name'] = self.file_name
        self.params['output_folder'] = self.file_path
        super().__init__(self.params)

    def exist_test(self):
        self.log.write("info", "Start of search operation")
        try:
            file = Path(self.file_path)
            if file.is_file():
                self.log.write("info", "File " + self.file_name + " detected", val="search")
                return 0
            else:
                self.log.write("info", "File " + self.file_name + " not detected", val="search")
                return 1

        except Exception as e:
            self.log.write("error", str(e))
            return 1

    def exit_code(self):
        self.exit = self.exist_test()
        self.log.write("info", "exit code: " + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_exists = Exists(args.file_name, args.path)
    test_exists.exit_code()
