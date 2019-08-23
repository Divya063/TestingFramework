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
import threading
from TestBase import Test
import _thread as thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--name", dest="name",
                        required=False,
                        help='name')
    parser.add_argument("--timeout", type=int,
                        required=False,
                        help='timeout')

    args = parser.parse_args()
    return args


client = docker.client.from_env()


class Docker(Test):
    """Test to check if user container is healthy"""

    def __init__(self, container_name, timeout):
        self.timeout = timeout
        self.ref_test_name = "container"
        self.container_name = container_name
        super().__init__()

    def quit_function(self, fn_name):
        self.log.write("error", '{0} took too long'.format(fn_name))
        exit(1)

    def run_test(self):
        timer = threading.Timer(self.timeout, self.quit_function, args=['check_container'])
        timer.start()
        # start docker events
        try:
            events = client.events(decode=True)
            # exec into container and run a command
            output = client.containers.get(self.container_name).exec_run(cmd=["bin/ls", "-A"], workdir="/",
                                                                         stdout=True)
        except Exception as exc:
            self.log.write("error", str(exc))
            return 1
        else:
            self.log.write("info", str(output))
            exit_code = output[0]
            msg = output[1].decode("utf-8")
            # On a successful exec there would be three events, if exec failed,
            # status "exec_die" would not appear, i.e. total events would be less than 3
            status_list = ['exec_create', 'exec_start', 'exec_die']
            for event_number, event in enumerate(events):
                self.log.write("info", str(event))
                # Checks if given status (given in the status_list) is present (inside events) or not
                if event['status'] != status_list[event_number] and not event['id']:
                    return 1
                if event_number == 2:
                    # to stop docker events, otherwise it would continue to listen
                    break
        finally:
            timer.cancel()

        self.log.write("info", "exit code :" + str(exit_code))
        return exit_code


if __name__ == "__main__":
    args = get_args()
    test_container = Docker(args.name, args.timeout)
    (test_container.run_test())
