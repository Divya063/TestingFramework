import os
import time
from IOUtils import ReadWriteOp
import sys

sys.path.append("..")
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from TestBase import Test
from timer import StopWatch, Measure, Profiling
import argparse

dictionary = {}
extension = ".txt"


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


class Throughput(Test):
    """Return read and write throughput for a given number of files"""

    def __init__(self, number_of_files, input_size, dest_path):
        self.number_of_files = number_of_files
        self.input_size = input_size
        self.storage_path = dest_path
        self.file_path = os.path.join("/", dest_path)
        self.ops = ReadWriteOp()
        self.ref_test_name = "throughput"
        self.params = {}
        self.params['number_files'] = self.number_of_files
        self.params['file_size'] = self.input_size
        self.params['output_folder'] = self.file_path
        super().__init__(self.params)

    def check_directory(self):

        if not (os.path.isdir(self.file_path)):
            self.log.write("error", "eos directory does not exist")
            return 1
        else:
            self.log.write("info", "eos directory exists, check passed...")
            return 0

    def write_test(self, number_of_files, input_size):
        self.log.write("info", "Creating workload...")
        payload = self.ops.generate_payload(number_of_files, input_size)
        self.log.write("info", "Workload created")
        timer = Profiling()
        self.log.write("info", "Begin of write operations...")
        self.log.write("performance", "\t".join(
            ["file_name", "file_size", "elapsed(s)", "through(MB/s)", "start-time", "end-time"]), val="read")
        for files, content in enumerate(payload):
            name = files
            file_name = str(name) + extension
            dest = self.file_path + file_name
            try:
                measure = timer.stats.startMeasurement()
                self.ops.plain_write(dest, content)  # write function
                measure.s1top()
                # measure val returns start time, end time and total duration
                val = measure.val()

            except Exception as err:
                self.log.write("error", "Error while writing " + file_name)
                self.log.write("error", file_name + ": " + str(err))
                return 1

            else:
                size, fsize = self.ops.convert_size(input_size)
                self.log.write("performance", "\t".join(
                    [file_name, str(input_size), str("%.8f" % float(val[2])),
                     str("%.4f" % float(self.ops.set_performance(val[2], fsize))), str(val[0]), str(val[1])]),
                               val="write")
                stats = timer
                self.log.write("info", str(stats), val="write")
                return 0

    def read_test(self, number_of_files):
        """

        :param number_of_files:
        :return: read throughput
        """

        timer = Profiling()
        self.log.write("info", "Begin of read operations...")
        self.log.write("performance", "\t".join(
            ["file_name", "file_size", "elapsed(s)", "through(MB/s)", "start-time", "end-time"]), val="read")
        for count in range(number_of_files):
            file_name = str(count) + extension
            dest = self.file_path + file_name
            try:
                measure = timer.stats.startMeasurement()
                self.ops.plain_read(dest)
                measure.stop()
                val = measure.val()
            except Exception as err:
                self.log.write("error", "Error while reading " + file_name)
                self.log.write("error", file_name + ": " + str(err))
                return 1
            else:
                size, fsize = self.ops.convert_size(self.input_size)
                self.log.write("performance", "\t".join(
                    [file_name, str(self.input_size), str(("%.8f" % float(val[2]))),
                     str(("%.4f" % float(self.ops.set_performance(val[2], fsize)))), str(val[0]),
                     str(val[1])]), val="read")
                stats = str(timer)
                self.log.write("info", stats, val="read")
                return 0

    def exit_code(self):
        self.check_dir = self.check_directory()
        if self.check_dir == 1:
            self.exit = 1
        else:
            write_t = self.write_test(self.number_of_files, self.input_size)
            read_t = self.read_test(self.number_of_files)
            self.exit |= write_t
            self.exit |= read_t
        self.log.write("info", "exit code: " + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_throughput = Throughput(args.number, args.file_size, args.path)
    test_throughput.exit_code()
