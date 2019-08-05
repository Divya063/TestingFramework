import json
import requests
import subprocess
import os
import sys
import argparse
import docker

sys.path.append("..")
import time
from logger import Logger, LOG_FOLDER, LOG_EXTENSION
from TestBase import Test
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--name", dest="name",
                        required=False,
                        help='name')

    args = parser.parse_args()
    return args


client = docker.client.from_env()


class Docker(Test):
    """Test to check if user container is healthy"""

    def __init__(self, container_name):
        self.ref_test_name = "container"
        self.container_name = container_name
        super().__init__()

    def check_container(self):
        # start docker events
        events = client.events(decode=True)
        # exec into container and run a command
        output = client.containers.get(self.container_name).exec_run(cmd=["bash", "-c", "ls -A "], workdir="/",
                                                                     stdout=True)
        exit_code = output[0]
        msg = output[1].decode("utf-8")
        status_list = ['exec_create', 'exec_start', 'exec_die']
        event_number = 0
        for event in events:
            self.log.write("info", str(event))
            # Checks if given status (given in the status_list) is present (inside events) or not
            if event['status'] != status_list[event_number] and not event['id']:
                return 1
            event_number = event_number + 1
            if event_number == 3:
                break

        self.log.write("info", "exit code :" + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_container = Docker(args.name)
    (test_container.check_container())
