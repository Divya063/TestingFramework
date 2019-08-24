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
from TestBase import Test
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dest", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args


class Delete(Test):
    """Checks if a file gets deleted or not"""

    def __init__(self, filePath):
        self.ref_test_name = "Delete"
        self.file_path = filePath
        self.file_path = os.path.join("/", filePath)
        self.params = {}
        self.params['file_path'] = self.file_path
        super().__init__(**self.params)

    def run_test(self):
        exit_code = 0
        try:
            self.log.write("info", "Start of delete operation")
            os.remove(self.file_path)
        except OSError as e:
            self.log.write("error", "Error: %s." % e.strerror)
            exit_code = 1
        else:
            self.log.write("info", "File " + self.file_path + " successfully deleted", val="delete")

        self.log.write("info", "overall exit code " + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_delete = Delete(args.path)
    test_delete.run_test()
