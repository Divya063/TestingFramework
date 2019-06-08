import os
import sys
from IOUtils import ReadWriteOp, ChecksumCal
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
        self.parentDirectory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.file_path = os.path.join(self.parentDirectory, self.eos_path)
        self.ops = ReadWriteOp()
        self.check = ChecksumCal()
        self.exit = 0


    def checksum_test(self, number_of_files, input_size):
        """

        :param number_of_files:
        :param input_size:
        :return:
        """
        corrupted_files = 0
        payload = self.ops.generate_payload(number_of_files, input_size)
        for files, content in enumerate(payload):
            name = files
            file_name = str(name) + extension
            dest = self.file_path + file_name
            try:
                hash_num = self.check.calculate_hash(content)
                print(hash_num)
                self.ops.plain_write(dest, content)  # write function
                data = self.ops.plain_read(dest)
                returned_hash = self.check.calculate_hash(data)
                print(returned_hash)
                if(returned_hash != hash_num):
                    corrupted_files +=1
            except Exception as err:
                self.exit |= 1

        return corrupted_files


    def exit_code(self):
        if(self.checksum_test(self.number_of_files, self.input_size)>0):
                self.exit|=1
        return self.exit

if __name__ == "__main__":
    args = get_args()
    test_integrity =  Checksum(args.number, args.file_size, args.path)
    print(test_integrity.exit_code())


