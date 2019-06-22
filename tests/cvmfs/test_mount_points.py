"""
Run using the command:

python3 test_mount_points.py --repo_name sft.cern.ch --path cvmfs/sft.cern.ch --container cvmfs

"""

import docker
import argparse
import sys
from tests.cvmfs.test_mount_container import MountContainer
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

class MountPoint:
    def __init__(self, repo_name, repo_path, container):
        self.check_mount = MountContainer.check_mount(repo_name, repo_path, container)
        self.check_empty = MountContainer.check_empty(repo_name, repo_path, container)
        self.container = container

    def check_config_status(self, container):
        output_status = client.containers.get(container).exec_run(cmd=["bash", "-c", "cvmfs_config status"],
                                                               stdout=True)

        """
        ExecResult(exit_code=0, output=b'sft.cern.ch mounted on /cvmfs/sft.cern.ch with pid 82\nsft-nightlies.cern.ch mounted on /cvmfs/sft-nightlies.cern.ch with pid 148\n')

        """
        #files = output_status[1].decode("utf-8")
        print(output_status)



    def check_config_probe(self, container):
        output_probe = client.containers.get(container).exec_run(cmd=["bash", "-c", "cvmfs_config probe"],
                                                                  stdout=True)
        """
        result format
        ExecResult(exit_code=0, output=b'Running /usr/bin/cvmfs_config stat sft.cern.ch:
        VERSION PID UPTIME(M) MEM(K) REVISION EXPIRES(M) NOCATALOGS CACHEUSE(K) CACHEMAX(K) 
        NOFDUSE NOFDMAX NOIOERR NOOPEN HITRATE(%) RX(K) SPEED(K/S) HOST PROXY ONLINE
        2.4.1.0 82 1689 41396 14822 0 202 444516 10240001 0 65024 0 259023 99.2144 185038 0 
        http://cvmfs-stratum-one.cern.ch/cvmfs/sft.cern.ch DIRECT 1
        
        Running /usr/bin/cvmfs_config stat sft-nightlies.cern.ch:
        VERSION PID UPTIME(M) MEM(K) REVISION EXPIRES(M) NOCATALOGS CACHEUSE(K) CACHEMAX(K) NOFDUSE NOFDMAX NOIOERR NOOPEN HITRATE(%) RX(K) SPEED(K/S) HOST PROXY ONLINE
        2.4.1.0 148 1689 22728 26641 1 1 444516 10240001 0 65024 0 0 n/a 107 0 http://cvmfs-stratum-one.cern.ch/cvmfs/sft-nightlies.cern.ch DIRECT 1\n')

        """
        #exit_code
        return output_probe[0]

    def check_config_stat(self, container):
        output_stat = client.containers.get(container).exec_run(
            cmd=["bash", "-c", "cvmfs_config stat"], stdout=True)
        # result format
        """
        ExecResult(exit_code=0, output=b'cvmfs2 on /cvmfs/sft.cern.ch type fuse 
        (ro,nosuid,nodev,relatime,user_id=0,group_id=0,default_permissions,allow_other)\n')

        """
        # exit_code
        return output_stat[0]



    def exit_code(self):
        code= self.check_mount
        code |=self.check_empty
        if(code==0):
            code |=self.check_config_probe(self.container)
            code |=self.check_config_stat(self.container)
            code |=self.check_config_status(self.container)
        return code


if __name__ == "__main__":
    args = get_args()
    test_mount = MountPoint(args.repo_name, args.path, args.container)
    test_mount.exit_code()