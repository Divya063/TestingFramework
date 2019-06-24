import os
import time
from IOUtils import ReadWriteOp
import sys
sys.path.append("..")
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from timer import Profiling
import argparse
<<<<<<< HEAD
=======

>>>>>>> codesfixes

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
        self.exit = None
        self.ref_timestamp = int(time.time())
        self.input_size = input_size
        self.eos_path = dest_path
        self.ref_test_name = 'throughput'
        #self.parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
<<<<<<< HEAD
        """
        In user container os.path.expanduser('~') is equal to '/eos/user/u/user2'
        """
        self.file_path = os.path.expanduser('~')
=======
        self.file_path= os.path.expanduser('~')
>>>>>>> codesfixes
        #self.file_path = os.path.join(self.parentDirectory, self.eos_path)
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.ops = ReadWriteOp()
        self.log.write("info", self.ref_test_name + " Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.log_params()

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


    def write_test(self, number_of_files, input_size):
        self.log.write("info", "Creating workload...")
        payload = self.ops.generate_payload(number_of_files, input_size)
        self.log.write("info", "Workload created")
        timer = Profiling()
        self.log.write("info", "Begin of write operations...")
        self.log.write("performance", "\t".join(
            ["file_name", "file_size", "elapsed(s)", "through(MB/s)", "start-time", "end-time"]), val = "read")
        for files, content in enumerate(payload):
            name = files
            file_name = str(name) + extension
            dest = self.file_path + file_name
            try:
                measure = timer.stats.startMeasurement()
                self.ops.plain_write(dest, content) #write function
                measure.stop()
                #measure val returns start time, end time and total duration
                val = measure.val()

            except Exception as err:
                self.log.write("error", "Error while writing " + file_name)
                self.log.write("error", file_name+ ": " + str(err))
                self.exit |=1

            else:
                size, fsize = self.ops.convert_size(input_size)
                self.log.write("performance", "\t".join(
                    [file_name, str(input_size), str("%.8f" % float(val[2])), str("%.4f" % float(self.ops.set_performance(val[2], fsize))), str(val[0]), str(val[1])]), val = "write")
        stats = timer
        self.log.write("info", str(stats), val = "write")
        self.log.write("info", "End of write operations")
        return stats

    def read_test(self, number_of_files):
        """

        :param number_of_files:
        :return: read throughput
        """

        timer = Profiling()
        self.log.write("info", "Begin of read operations...")
        self.log.write("performance", "\t".join(
            ["file_name", "file_size", "elapsed(s)", "through(MB/s)", "start-time", "end-time"]), val = "read")
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
                self.exit|=1
            else:
                size, fsize = self.ops.convert_size(self.input_size)
                self.log.write("performance", "\t".join(
                    [file_name, str(self.input_size), str(("%.8f" % float(val[2]))), str(("%.4f" % float(self.ops.set_performance(val[2], fsize)))), str(val[0]),
                     str(val[1])]), val = "read")
        stats = str(timer)
        self.log.write("info", stats, val ="read")
        self.log.write("info", "End of read operations")
        return stats

    def exit_code(self):
        self.check_dir = self.check_directory()
        if (self.check_dir == 1):
            self.exit |= 1
        else:
            write_t = self.write_test(self.number_of_files, self.input_size)
            read_t = self.read_test(self.number_of_files)
            if not write_t :
                self.exit |=1
            if not read_t:
                self.exit |=1
        self.log.write("info", "exit code: " + str(self.exit))
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_throughput = Throughput(args.number, args.file_size, args.path)
    test_throughput.exit_code()


