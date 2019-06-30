


"""
Run using the command:

python3 test_mount_points.py --repo_name sft.cern.ch --path cvmfs/sft.cern.ch --container cvmfs

"""
import os
import time
import argparse
import sys
import subprocess

sys.path.append('..')
from logger import Logger, LOG_FOLDER, LOG_EXTENSION


class ConfigStat:
    def __init__(self):
        self.ref_timestamp = int(time.time())
        self.ref_test_name = "config_stat"
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name +"_" + time.strftime("%Y-%m-%d_%H:%M:%S")+ LOG_EXTENSION))
        self.log.write("info", "Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.code = 0
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))

    def check_config_stat(self):
        self.log.write("info", "Running command cvmfs_config probe")
        try:
            output = subprocess.check_output(
                ['cvmfs_config', 'stat'], stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            self.log.write("error", "Status : FAIL", exc.returncode, exc.output)
            self.code = exc.returncode
        else:
            self.log.write("info", "Output: \n{}\n".format(output))

        self.log.write("info", "Exit code " + str(self.code))
        return self.code

    def exit_code(self):
        self.code |= self.check_config_stat()
        self.log.write("info", "Overall exit code " + str(self.code))
        return self.code

if __name__ == "__main__":
    test_config_probe = ConfigStat()
    test_config_probe.exit_code()