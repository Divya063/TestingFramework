import hashlib
import os
import glob
import traceback
import re
import binascii
import logging
from IOUtils import ReadWriteOp, Checksum
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
    args = parser.parse_args()
    return args


class Benchmark():

    def __init__(self, number_of_files, input_size):
        self.number_of_files = number_of_files
        self.exit = 0
        self.input_size = input_size
        self.ops = ReadWriteOp()
        self.check = Checksum()
        #self.check_dir = self.check_directory()
        self.write_result = self.write_test(number_of_files, input_size)
        self.read_result = self.read_test(number_of_files)


    def check_directory(self):
        if not (os.path.isdir("eos")):
            return 1
        return 0

    def write_test(self, number_of_files, input_size):
        """

        :param number_of_files:
        :param input_size:
        :return: write throughput
        """
        size, bytes_required = self.ops.convert_size(input_size)
        timer = Profiling()
        for files in range(number_of_files):
            name = files
            file_name = str(name) + extension
            try:
                with open(file_name, 'wb') as fout:
                    content = os.urandom(size * bytes_required)
                    hash_num = self.check.calculate_source_hash(content)
                    measure = timer.stats.startMeasurement()
                    fout.write(content)
                    measure.stop()
                dictionary[file_name] = hash_num
            except IOError:
                self.exit |=1
        timer.stop()
        return timer

    def read_test(self, number_of_files):
        """

        :param number_of_files:
        :return: read throughput
        """
        global file_size
        output = open("output.txt", "w+")
        output.write("%s %s %s\n" % ("name", "size", "corruption_boolean"))
        timer = Profiling()
        for count in range(number_of_files):
            file_name1 = str(count) + extension
            """
            corruption_boolean = "NO" indicates the file is not corrupted
            """
            corruption_boolean = "NO"
            try:
                with open(file_name1, 'rb') as text_file:
                    statinfo = os.stat(file_name1)
                    file_size = self.ops.convert_bytes(statinfo.st_size)
                    measure = timer.stats.startMeasurement()
                    random_data = text_file.read()
                    measure.stop()
                    # checks the integrity of the file by comparing the hashed values
                    dest_checksum= self.check.calculate_dest_hash(file_name1)
                    if (dest_checksum != dictionary[file_name1]):
                        corruption_boolean = "YES"
            except IOError:
                corruption_boolean = "YES"
                self.exit|=1
                traceback.print_exc()
            output.write("%s %s %s\n" % (file_name1, file_size, corruption_boolean))
        output.close()
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
    test_throuput = Benchmark(args.number, args.file_size)
    print(test_throuput.exit_code())
    test_throuput.print_result()


