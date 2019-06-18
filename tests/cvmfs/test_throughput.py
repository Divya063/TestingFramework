import os
import argparse
import subprocess
import time
from tests.logger import Logger, LOG_FOLDER, LOG_EXTENSION


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--num", dest="num_packages",
                        required=True,
                        help='Number of packages')

    parser.add_argument("--path", dest="path",
                        required=True,
                        help='Specify the path')
    args = parser.parse_args()
    return args

class Throughput:
    def __init__(self, num_packages, repo_path):
        self.number = num_packages
        self.repo_path = repo_path


    def read(self, num_packages, repo_path):

