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
from test_main import Test
import argparse


extension = ".txt"

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( "--file_name", dest="file_name",
                        required = True,
                        help='Name of the file')
    parser.add_argument("--dest", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args


class Delete(Test):
    """

    Checks if a file gets deleted or not
    """

    def __init__(self, file_name, dest_path):
        self.ref_timestamp = int(time.time())
        self.storage_path = dest_path
        self.file_name = file_name
        #self.parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.root_file_path= os.path.join("/", dest_path)
        self.file_path = os.path.join(self.root_file_path, file_name)
        #self.file_path = os.path.join(self.parentDirectory, self.eos_path)
        params = {}
        params['test_name'] = "Delete"
        params['File name'] = self.file_name
        params['Typed output folder'] = self.file_path
        Test.__init__(self, **params)


    def delete_test(self):
        try:
            self.log.write("info", "Start of delete operation")
            os.remove(self.file_path)
        except OSError as e:
            self.log.write("error", "Error: %s - %s." % (e.filename, e.strerror))
            self.exit =1
        else:
            self.log.write("info", "File "+ self.file_name + " successfully deleted",  val = "delete")
            self.exit = 0
        self.log.write("info", "End of delete operation")
        return self.exit


    def exit_code(self):
        self.exit = self.delete_test()
        self.log.write("info", "exit code: " + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_delete = Delete(args.file_name, args.path)
    test_delete.exit_code()


