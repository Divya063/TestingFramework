import hashlib
import os
import glob
import traceback
import re
import binascii
import logging
import time
from pathlib import Path
from IOUtils import ReadWriteOp
import sys

sys.path.append("..")
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from TestBase import Test
import argparse

extension = ".txt"


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--file_size", dest="file_size",
                        required=True,
                        help='Size of the files, eg - 1M FOR 1MB, 2K for 2KB')
    parser.add_argument("--dest", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args


class Write(Test):
    """Writes to a file (of a given size) in the specified path"""

    def __init__(self, fileSize, filePath):
        self.input_size = fileSize
        self.storage_path = filePath
        self.file_path = os.path.join("/", filePath)
        self.ops = ReadWriteOp()
        self.ref_test_name = "write"
        self.params = {}
        self.params['file_size'] = self.input_size
        self.params['output_folder'] = self.file_path
        super().__init__(**self.params)

    def run_test(self):
        self.log.write("info", "Creating workload...")
        payload = self.ops.generate_payload(1, self.input_size)
        self.log.write("info", "Workload created")
        self.log.write("info", "Begin of write operations...")
        exit_code = 0
        for files, content in enumerate(payload):
            name = files
            file_name = str(name) + extension
            dest = self.file_path + file_name
            try:
                self.ops.plain_write(dest, content)  # write function
            except Exception as err:
                self.log.write("error", "Error while writing " + file_name)
                self.log.write("error", file_name + ": " + str(err))
                exit_code = 1


            else:
                size, fsize = self.ops.convert_size(self.input_size)
                self.log.write("info", "File " + file_name + " of size " + self.input_size + " successfully written",
                               val="write")

        self.log.write("info", "overall exit code " + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_write = Write(args.file_size, args.path)
    test_write.run_test()
