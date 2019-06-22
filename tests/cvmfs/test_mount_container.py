"""
Run using the command:

python3 test_mount_points.py --repo_name sft.cern.ch --path cvmfs/sft.cern.ch --container cvmfs

"""
import os
import time
import docker
from io import BytesIO
import argparse
import sys
sys.path.append('..')
from logger import Logger, LOG_FOLDER, LOG_EXTENSION



client = docker.client.from_env()

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--repo_name", dest="repo_name",
                        required=True,
                        help='Repository name'
                        )
    parser.add_argument("--path", dest="path",
                        required=True,
                        help='Specify the path')
    parser.add_argument("--container", dest="container",
                        required=True,
                        help='Container name')
    args = parser.parse_args()
    return args

class MountContainer:
    def __init__(self, repo_name, repo_path, container):
        self.repo_name = repo_name
        self.repo_path = repo_path
        self.container = container
        self.ref_timestamp = int(time.time())
        self.ref_test_name = "mount_container"
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log1 = Logger(os.path.join(self.logger_folder, self.ref_test_name + LOG_EXTENSION))
        self.log1.write("info", "Tests starting...")
        self.log1.write("info", time.strftime("%c"))
        self.code =0
        self.log1_params()


    def log1_params(self):
        self.log1.write("parameters", "Test name: " + self.ref_test_name)
        self.log1.write("parameters", "Test time: " + str(self.ref_timestamp))

    def check_empty(self, repo_path, container):
        self.log1.write("info", "Checking if directory is empty")
        output_empty = client.containers.get(container).exec_run(cmd=["bash", "-c", "ls -A "+ repo_path+ " | wc -l"],
                                                               stdout=True)
        """
        result format
        ExecResult(exit_code=0, output=b'6\n')
        """
        files = output_empty[1].decode("utf-8")
        #print(files)
        if(files==0):
            self.log1.write("error", "Directory is empty")
            self.log1.write("info", "exit code" + str(1))
            self.code |=1
        self.log1.write("info", "Directory is not empty")
        self.log1.write("info", "Status code "+ str(output_empty[0]))



    def check_mount(self, repo_path, container):
        self.log1.write("info", "Checking if repository is mounted")
        output_mount = client.containers.get(container).exec_run(
            cmd=["bash", "-c", "mount -l | grep "+repo_path], stdout=True)
        #result format
        """
        ExecResult(exit_code=0, output=b'cvmfs2 on /cvmfs/sft.cern.ch type fuse 
        (ro,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,allow_other)\n')

        """
        if(output_mount[0]==1):
            self.log1.write("error", "Repository is not mounted")
            self.log1.write("info", "Exit code "+ str(1))
            return 1
        self.log1.write("error", "Repository mounted")
        self.log1.write("info", "Exit code " + str(output_mount[0]))
        self.check_empty(repo_path, container)
        #exit_code
        self.code |=output_mount[0]
        return self.code

    def exit_code(self):
        self.code= self.check_mount(self.repo_path, self.container)
        self.log1.write("info", "Overall Exit code " + str(self.code))
        return self.code


if __name__ == "__main__":
    args = get_args()
    test_mount = MountContainer(args.repo_name, args.path, args.container)
    test_mount.exit_code()