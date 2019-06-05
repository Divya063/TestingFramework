import hashlib
import os
import glob
import traceback
import re
import binascii
import logging
from .timer import StopWatch, Measure, Profiling

BLOCKSIZE = 65536

dictionary = {}
extension = ".txt"

class Benchmark():

    def __init__(self, number_of_files, input_size):
        self.number_of_files = number_of_files
        self.input_size = input_size
        self.write_result = self.write_test(number_of_files, input_size)
        self.read_result = self.read_test(number_of_files)
        self.corruption_result=self.corruption_test()

    # SHA256 Hash (also handles Large Files)
    def calculate_hash(self, file):
        hasher = hashlib.sha256()
        with open(file, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return (hasher.hexdigest())


    def convert_bytes(self, num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.1f %s" % (num, x)
            num /= 1024.0


    def extract_digits(self, s):
        """
        this function separates digits and strings
        """
        string = s.strip('0123456789')
        digit = int(re.search(r'\d+', s).group(0))
        return digit, string


    def convert_size(self, string):
        """
        this function calculates total bytes
        """
        units = ['K', 'M', 'G']
        requested_size, unit = self.extract_digits(string)
        # for conversion of lowercase to uppercase
        if (unit.islower()):
            unit = unit.upper()
        byte = 1
        if unit in units:
            for i in range(units.index(unit) + 1):
                byte *= 1024
        return requested_size, byte

    def write_test(self, number_of_files, input_size):
        """

        :param number_of_files:
        :param input_size:
        :return: write throughput
        """
        size, bytes_required = self.convert_size(input_size)
        timer = Profiling()
        for files in range(number_of_files):
            name = files
            file_name = str(name) + extension
            with open(file_name, 'wb') as fout:
                # create files filled with random bytes
                measure=timer.stats.startMeasurement()
                content = os.urandom(size * bytes_required)
                hash_num = hashlib.sha256(content).hexdigest()
                fout.write(content)
                measure.stop()
            dictionary[file_name] = hash_num
        timer.stop()
        return timer

    def read_test(self, number_of_files):
        """

        :param number_of_files:
        :return: read throughput
        """
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
                    file_size = self.convert_bytes(statinfo.st_size)
                    measure = timer.stats.startMeasurement()
                    random_data = text_file.read()
                    measure.stop()
                    # checks the integrity of the file by comparing the hashed values
                    if (self.calculate_hash(file_name1) != dictionary[file_name1]):
                        corruption_boolean = "YES"

            except IOError:
                corruption_boolean = "YES"
                traceback.print_exc()
            output.write("%s %s %s\n" % (file_name1, file_size, corruption_boolean))
        output.close()
        timer.stop()
        return timer

    def corruption_test(self):
        """

        :return: number of corrupted files
        """
        flag = 0
        corrupted_files = 0
        with open('output.txt', 'rb') as text:
            for line in text:
                string = line.decode('utf-8', 'ignore')
                if (flag == 1):
                    list = string.split(" ")
                    if (list[3].strip() == "YES"):
                        # counts number of corrupted files
                        corrupted_files += 1
                flag = 1

        return corrupted_files

    def print_result(self):
        result=('\n\nWritten {} in {} files\n {}'.format(
            self.input_size, self.number_of_files, self.write_result))
        result+=('\n\nRead {} files having {} data each\n {}\n\nCorruption stats:\n{} files are corrupted'.format(
            self.number_of_files, self.input_size, self.read_result, self.corruption_result))

        print(result)
        return result

