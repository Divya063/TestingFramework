import os, sys
import argparse
import glob
import logging
import yaml
from yaml import load
import time

from EOS.test_throughput import Benchmark

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        required=False,
                        help='name of the test you want to run')
    parser.add_argument('-j', '--json',
                        required=False,
                        action='store',
                        help='Output to json file')
    args = parser.parse_args()
    return args

def cleanup():
    """
    delete the created files
    """
    filelist = glob.glob(os.path.join("", "*.txt"))
    for f in filelist:
        os.remove(f)

def get_config(cfg):
    with open(cfg, 'r') as stream:
        return yaml.safe_load(stream)


def main():
    tasks = get_config('test.yaml')
    print(tasks['tests']['storage']['throughput']['fileNumber'])
    args = get_args()
    logging.basicConfig(level=logging.INFO, filename='test.log', filemode='w',
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logging.info('Started')
    logger = logging.getLogger(args.test)
    if(args.test=="EOS"):
        print("Enter the number of files")
        number_of_files = int(input())
        print("Enter size (in whole number)")
        print("Example:\n 1M for 1 MB\n 5K for 5 KB\n 1G for 1 GB\n1024 for 1 KB")
        size = input()
        test = Benchmark(number_of_files, size)
        logger.info(test.print_result())

    cleanup()
    logging.info('Finished')

if __name__ == "__main__":
    main()
