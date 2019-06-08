import hashlib
import os
import glob
import traceback
import re
import binascii
import logging
from IOUtils import ReadWriteOp
from timer import StopWatch, Measure, Profiling
import argparse
import sys

dictionary = {}
extension = ".txt"

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


class Throughput():

    def __init__(self, number_of_files, input_size, dest_path):
        self.number_of_files = number_of_files
        self.exit = 0
        self.input_size = input_size
        self.eos_path = dest_path
        self.parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.file_path = os.path.join(self.parentDirectory, self.eos_path)
        print(self.file_path)
        self.ops = ReadWriteOp()
        self.write_result = self.write_test(number_of_files, input_size)
        self.read_result = self.read_test(number_of_files)


    def check_directory(self):
        if not (os.path.isdir("eos")):
            return 1
        return 0

    def write_test(self, number_of_files, input_size):
        payload = self.ops.generate_payload(number_of_files, input_size)
        timer = Profiling()
        for files, content in enumerate(payload):
            name = files
            file_name = str(name) + extension
            dest = self.file_path + file_name
            try:
                measure = timer.stats.startMeasurement()
                self.ops.plain_write(dest, content) #write function
                measure.stop()
            except Exception as err:
                self.exit |=1
        timer.stop()
        return timer

    def read_test(self, number_of_files):
        """

        :param number_of_files:
        :return: read throughput
        """

        timer = Profiling()
        for count in range(number_of_files):
            file_name = str(count) + extension
            dest = self.file_path + file_name
            try:
                measure = timer.stats.startMeasurement()
                self.ops.plain_read(dest)
                measure.stop()
            except Exception as err:
                self.exit|=1
                traceback.print_exc()
        timer.stop()
        return timer

    def exit_code(self):
        if (self.check_directory() == 1):
            self.exit |= 1
        else:
            if not self.write_result:
                self.exit |=1
            if not self.read_result:
                self.exit |=1
        return self.exit


    def print_result(self):
        result=('\n\nWritten {} in {} files\n {}'.format(
            self.input_size, self.number_of_files, self.write_result))
        result+=('\n\nRead {} files having {} data each\n {}'.format(
            self.number_of_files, self.input_size, self.read_result))

        print(result)
        return result


if __name__ == "__main__":
    args = get_args()
    test_throuput = Throughput(args.number, args.file_size, args.path)
    print(test_throuput.exit_code())
    test_throuput.print_result()


