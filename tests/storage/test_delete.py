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

    def __init__(self, file_path):
        self.ref_test_name = "Delete"
        self.file_path = self.file_path
        self.params = {}
        self.params['file_path'] = self.file_path
        super().__init__(**self.params)

    def delete_test(self):
        try:
            self.log.write("info", "Start of delete operation")
            os.remove(self.file_path)
        except OSError as e:
            self.log.write("error", "Error: %s." % e.strerror)
            return 1
        else:
            self.log.write("info", "File " + self.file_path + " successfully deleted", val="delete")
            return 0

    def exit_code(self):
        self.exit = self.delete_test()
        self.log.write("info", "exit code: " + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_delete = Delete(args.path)
    test_delete.exit_code()
