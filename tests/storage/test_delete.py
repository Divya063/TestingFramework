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


class Delete():

    def __init__(self, file_name, dest_path):
        self.exit = 0
        self.ref_timestamp = int(time.time())
        self.storage_path = dest_path
        self.ref_test_name = 'delete'
        self.file_name = file_name
        #self.parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.root_file_path= os.path.join("/", dest_path)
        self.file_path = os.path.join(self.root_file_path, file_name)
        #self.file_path = os.path.join(self.parentDirectory, self.eos_path)
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log.write("info", self.ref_test_name + " Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "File name: " + self.file_name)
        self.log.write("parameters", "Typed output folder: " + self.file_path)
        self.log.write("parameters", "Logger folder: " + self.logger_folder)


    def delete_test(self):
        try:
            self.log.write("info", "Start of delete operation")
            os.remove(self.file_path)
        except OSError as e:
            self.log.write("error", "Error: %s - %s." % (e.filename, e.strerror))
            self.exit |=1
        else:
            self.log.write("info", "File "+ self.file_name + " successfully deleted",  val = "delete")
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


