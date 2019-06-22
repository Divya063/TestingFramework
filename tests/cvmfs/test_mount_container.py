"""
Run using the command:

python3 test_mount_points.py --repo_name sft.cern.ch --path cvmfs/sft.cern.ch --container cvmfs

"""
import docker
from io import BytesIO
import argparse
import sys
sys.path.append('...')


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

    def check_empty(self, repo_path, container):
        output_empty = client.containers.get(container).exec_run(cmd=["bash", "-c", "ls -A "+ repo_path+ " | wc -l"],
                                                               stdout=True)
        """
        result format
        ExecResult(exit_code=0, output=b'6\n')
        """
        files = output_empty[1].decode("utf-8")
        #print(files)
        if(files==0):
            return output_empty[0]|1
        return output_empty[0]



    def check_mount(self, repo_path, container):
        output_mount = client.containers.get(container).exec_run(
            cmd=["bash", "-c", "mount -l | grep "+repo_path], stdout=True)
        #result format
        """
        ExecResult(exit_code=0, output=b'cvmfs2 on /cvmfs/sft.cern.ch type fuse 
        (ro,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,allow_other)\n')

        """
        #exit_code
        return output_mount[0]

    def exit_code(self):
        code= self.check_mount(self.repo_path, self.container)
        code|=self.check_empty(self.repo_path, self.container)
        return code


if __name__ == "__main__":
    args = get_args()
    test_mount = MountContainer(args.repo_name, args.path, args.container)
    test_mount.exit_code()