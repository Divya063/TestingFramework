import os
import glob
from test_throughput import Throughput
from test_checksum import Checksum


def run_storage(tasks):
    """
     Helper function for running storage test suite
    """
    test_storage = tasks['tests']['storage']
    file_path = test_storage['statFile']['filepath']
    number_of_files = test_storage['throughput']['fileNumber']
    size = test_storage['throughput']['fileSize']
    exit_code = 0
    test_io = Throughput(number_of_files, size, file_path)
    exit_code |= test_io.exit_code()
    number_of_files = test_storage['checksum']['fileNumber']
    size = test_storage['checksum']['fileSize']
    test_integrity= Checksum(number_of_files, size, file_path)
    exit_code |= test_integrity.exit_code()
    return exit_code

