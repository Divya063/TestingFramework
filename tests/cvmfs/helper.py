import os
import glob
from test_mount import Mount
from test_throughput import Throughput
from test_ttfb import TTFB


def run_cvmfs(tasks):
    """
     Helper function for running CVMFS test suite
    """
    test_cvmfs = tasks['tests']['cvmfs']
    repo_path = test_cvmfs['mount']['repoPath']
    name_of_repo = test_cvmfs['mount']['repoName']
    lastUpdatePath = test_cvmfs['ttfb']['filePath']
    num_of_packages = test_cvmfs['throughput']['num']
    packages_path = test_cvmfs['throughput']['filePath']
    # Mount test
    test_mount = Mount(name_of_repo, repo_path)
    exit_code = 0
    exit_code |= test_mount.exit_code()
    # Time till first byte test
    test_ttfb = TTFB(repo_path, lastUpdatePath)
    exit_code |= test_ttfb.exit_code()
    # Throughput test
    test_throughput = Throughput(num_of_packages, repo_path, packages_path)
    exit_code |= test_ttfb.exit_code()
    return exit_code
