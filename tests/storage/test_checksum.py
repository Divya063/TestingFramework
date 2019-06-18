import os
import sys
from IOUtils import ReadWriteOp, ChecksumCal
from tests.logger import Logger, LOG_FOLDER, LOG_EXTENSION
import time
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--num", dest="number", type=int,
                        required=True,
                        help='Number of files to be generated')
    parser.add_argument( "--file_size", dest="file_size",
                        required = True,
                        help='Size of the files, eg - 1M FOR 1MB, 2K for 2KB')
    parser.add_argument("--dest", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args

dictionary = {}
extension = ".txt"

class Checksum:
    def __init__(self, number_of_files, input_size, dest_path):
        self.number_of_files = number_of_files
        self.input_size = input_size
        self.eos_path = dest_path
        self.ref_test_name = 'checksum'
        self.ref_timestamp = int(time.time())
        self.parentDirectory = os.path.expanduser('~')
        #print(self.parentDirectory)
        self.file_path = os.path.join(self.parentDirectory, self.eos_path)
        #print(self.file_path)
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name + LOG_EXTENSION))
        self.ops = ReadWriteOp()
        self.check = ChecksumCal()
        self.match = None
        self.log.write("info", "Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.exit = 0

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))
        self.log.write("parameters", "Number of files: " + str(self.number_of_files))
        self.log.write("parameters", "File size: " + str(self.input_size))
        self.log.write("parameters", "Typed output folder: " + self.file_path)
        self.log.write("parameters", "Logger folder: " + self.logger_folder)

    def check_directory(self):
        if not (os.path.isdir(self.file_path)):
            self.log.write("error", "eos directory does not exist")
            self.exit = 1
        else:
            self.log.write("info", "eos directory exists, check passed...")
            self.exit = 0
        return self.exit


    def checksum_test(self, number_of_files, input_size):
        """

        :param number_of_files:
        :param input_size:
        :return:
        """
        corrupted_files = 0
        self.log.write("info", "Creating workload...")
        payload = self.ops.generate_payload(number_of_files, input_size)
        self.log.write("info", "Workload created")
        self.log.write("info", "Begin of sanity check")
        self.log.write("consistency", "\t".join(["file_name", "matching", "source_checksum", "disk_checksum"]),
                       write_timestamp = True)
        for files, content in enumerate(payload):
            name = files
            file_name = str(name) + extension
            dest = self.file_path + file_name
            try:
                hash_num = self.check.calculate_hash(content)
                self.ops.plain_write(dest, content)  # write function
                data = self.ops.plain_read(dest) # read function
                returned_hash = self.check.calculate_hash(data)
                if(returned_hash != hash_num):
                    self.match = "False"
                    self.log.write(file_name + "is corrupted")
                    corrupted_files +=1
                else:
                    self.match = "True"
            except Exception as err:
                self.log.write("error",
                               "Unable to perform sanity check on " + file_name)
                self.log.write("error", file_name + ": " + str(err))
                self.exit |= 1
            else:
                self.log.write("consistency", "\t".join([file_name, self.match, hash_num, returned_hash]),
                               write_timestamp=True)

        self.log.write("info", "Number of corrupted files "+ str(corrupted_files))
        self.log.write("info", "End of sanity check")
        return corrupted_files


    def exit_code(self):
        if(self.checksum_test(self.number_of_files, self.input_size)>0):
                self.exit|=1
        self.log.write("info", "exit code: " + str(self.exit))
        return self.exit

if __name__ == "__main__":
    args = get_args()
    test_integrity =  Checksum(args.number, args.file_size, args.path)
    test_integrity.exit_code()


