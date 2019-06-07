import os
import glob
from test_throughput import Benchmark
from test_checksum import Corruption


def run_eos(tasks):
    """
     Helper function for running EOS test suite
    """
    test_storage = tasks['tests']['storage']
    number_of_files = test_storage['throughput']['fileNumber']
    size = test_storage['throughput']['fileSize']
    exit_code = 0
    test_io = Benchmark(number_of_files, size)
    print("Throughput Test\n exit code:%s "% (test_io.exit_code()))
    exit_code |= test_io.exit_code()
    test_integrity= Corruption()
    print("Integrity Test\n exit code:%s " % (test_integrity.exit_code()))
    exit_code |= test_integrity.exit_code()
    return exit_code

