import argparse
import glob
import os
import sys
import yaml
import subprocess

# run tests from user container

from tests.storage.helper import run_storage
from tests.jupyterhub_api.helper import run_jupyterhub_api
from tests.cvmfs.helper import run_cvmfs
from tests.database.helper import run_database

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        nargs='*', default='compTest',
                        required=True,
                        help='name of the test you want to run')
    args = parser.parse_args()
    return args


def get_config(cfg):
    if os.path.exists(cfg):
        with open(cfg, 'r') as stream:
            return yaml.safe_load(stream)
    else:
        raise Exception("yaml file not present")


def main():
    tasks = get_config('test.yaml')
    args = get_args()
    if args.test[0] == "storage":
        run_storage(tasks)
    if (args.test[0]) == "jupyterhub-api":
        run_jupyterhub_api(tasks)
    if (args.test[0]) == "CVMFS":
        run_cvmfs(tasks)
    if (args.test[0]) == "database":
        run_database(tasks)


if __name__ == "__main__":
    main()
