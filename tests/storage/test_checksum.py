import os
from IOUtils import ReadWriteOp, ChecksumCal
import sys

sys.path.append("..")
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from grafana import Grafana
from TestBase import Test
import time
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--num", dest="number", type=int,
                        required=True,
                        help='Number of files to be generated')
    parser.add_argument("--file_size", dest="file_size",
                        required=True,
                        help='Size of the files, eg - 1M FOR 1MB, 2K for 2KB')
    parser.add_argument("--dest", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args


extension = ".txt"


class Checksum(Test):
    """Calculates Checksum for a given number of files"""

    def __init__(self, fileNumber, fileSize, filePath):
        self.number_of_files = fileNumber
        self.input_size = fileSize
        self.storage_path = filePath
        self.file_path = os.path.join("/", filePath)
        self.ops = ReadWriteOp()
        self.check = ChecksumCal()
        self.match = None
        self.ref_test_name = "Checksum"
        self.params = {}
        self.params['number_files'] = self.number_of_files
        self.params['file_size'] = self.input_size
        self.params['output_folder'] = self.file_path
        super().__init__(**self.params)

    def run_test(self):
        """

        :param number_of_files:
        :param input_size:
        :return: Number of corrupted files
        """
        corrupted_files = 0
        self.log.write("info", "Creating workload...")
        payload = self.ops.generate_payload(self.number_of_files, self.input_size)
        self.log.write("info", "Workload created")
        self.log.write("info", "Begin of sanity check")
        self.log.write("consistency", "\t".join(["file_name", "matching", "source_checksum", "disk_checksum"])
                       )
        for files, content in enumerate(payload):
            name = files
            file_name = str(name) + extension
            dest = self.file_path + file_name
            try:
                hash_num = self.check.calculate_hash(content)
                self.ops.plain_write(dest, content)  # write function
                data = self.ops.plain_read(dest)  # read function
                returned_hash = self.check.calculate_hash(data)
                if returned_hash != hash_num:
                    self.match = "False"
                    self.log.write(file_name + "is corrupted")
                    corrupted_files += 1
                else:
                    self.match = "True"
            except Exception as err:
                self.log.write("error",
                               "Unable to perform sanity check on " + file_name)
                self.log.write("error", file_name + ": " + str(err))
                return 1
            else:
                self.log.write("consistency", "\t".join([file_name, self.match, hash_num, returned_hash]),
                               )

        self.log.write("info", "Number of corrupted files " + str(corrupted_files))
        self.log.write("info", "End of sanity check")
        exit_code = 1 if corrupted_files > 0 else 0
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_integrity = Checksum(args.number, args.file_size, args.path)
    test_integrity.run_test()
