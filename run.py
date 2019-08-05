import argparse
import glob
import os
import sys
import yaml
import pickle
import subprocess

from tests.storage.helper import run_storage
from helper import docker_cp_to_container, docker_cp_from_container, docker_exec
from tests.jupyterhub_api.helper import run_jupyterhub_api
from tests.cvmfs.helper import run_cvmfs
from tests.database.helper import run_database


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        nargs='*', default='compTest',
                        required=False,
                        help='name of the test you want to run')
    parser.add_argument('-c', '--configfile',
                        required=True,
                        help='load config file')

    parser.add_argument("-u", "--user_mode", action='store_true')

    parser.add_argument('-s', '--session',
                        required=False,
                        help='session name')

    parser.add_argument('-p', '--path',
                        required=False,
                        help='user path')
    args = parser.parse_args()
    return args


def get_config(cfg):
    if os.path.exists(cfg):
        with open(cfg, 'r') as stream:
            return yaml.safe_load(stream)
    else:
        raise Exception("yaml file not present")
        sys.exit()


def check_test_exists(directory, test_name):
    # Checks if mentioned tests exist in particular directory or not
    lists = ["statFile"]
    directory_path = os.path.join(os.getcwd(), 'tests')  # name of directory under which test exists
    if (test_name not in lists):
        test_file = "test_" + test_name + ".py"
        test_file_path = os.path.join(os.path.join(directory_path, directory), test_file)
        if not os.path.exists(test_file_path):
            raise Exception(test_name + " test file does not exists")


def check_input_validity(params):
    """
    Check the parameter type
    """
    string_val = ['filePath', 'fileSize', 'repoName', 'repoSize']
    int_val = ['fileNumber', 'num']
    for key, value in params.items():
        if key in int_val:
            if not type(value) == int:
                raise Exception(key + " having value %s is not a integer" % str(value))
        if key in string_val:
            if not type(value) == str:
                raise Exception(key + " having value %s is not a string" % str(value))


def validator(tasks):
    # To check validity of YAML File

    for key, test in tasks.items():
        # Exclude output configuration (present in test.yaml) from validation
        if key == "output":
            continue
        for directory, component_test in test.items():  # storage
            if component_test:
                for test_name, param in component_test.items():
                    if param:
                        check_test_exists(directory, test_name)
                        check_input_validity(param)


def cleanup():
    # delete the created files
    filelist = glob.glob(os.path.join("", "*.txt"))
    print(filelist)
    for f in filelist:
        os.remove(f)


def main():
    args = get_args()
    yaml_path = os.path.join(os.getcwd(), args.configfile)
    tasks = get_config(yaml_path)
    # These parameters are needed by 'TestBase.py' file for output conf
    #TODO
    # Look for an efficient method to pass these parameters to the 'TestBase.py' file
    with open('tests/tasks.pkl', 'wb') as f:
        pickle.dump(tasks, f)
    # Validates YAML File
    validator(tasks)
    if args.user_mode:
        if args.session == None:
            raise Exception("session argument needed")
        # container name
        container = "jupyter-" + args.session
        for test_name in args.test:
            if test_name == "storage":
                dir_path = os.path.join("/", os.path.join("scratch", args.session))
                docker_cp_to_container(container, dir_path)
                docker_exec(container, test_name, user=args.session, working_dir=dir_path)
                docker_cp_from_container(container, ":/scratch/", args.session)

            if test_name == "jupyterhub-api" or test_name == "database":
                container_name = "jupyterhub"
                docker_cp_to_container(container_name)
                docker_exec(container_name, test_name)
                docker_cp_from_container(container_name, ":/")

            if test_name == "CVMFS":
                docker_cp_to_container(container)
                docker_exec(container, test_name)
                docker_cp_from_container(container, ":/")

    else:
        # From host
        for test in args.test:
            if test == "storage":
                # passes the parameters loaded from yaml file to helper function
                run_storage(tasks)
                cleanup()

            if test == "jupyterhub-api":
                run_jupyterhub_api(tasks)

            if test == "CVMFS":
                run_cvmfs(tasks)

            if test == "database":
                run_database(tasks)


if __name__ == "__main__":
    main()
