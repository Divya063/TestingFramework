import argparse
import glob
import os
import sys
import yaml
import subprocess

from tests.storage.helper import run_storage
from tests.jupyterhub_api.helper import run_jupyterhub_api
from tests.cvmfs.helper import run_cvmfs
from helper import cp_helper


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        nargs='*', default='compTest',
                        required=False,
                        help='name of the test you want to run')
    parser.add_argument('-c', '--configfile',
                        required=False,
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

    directory_path = os.path.join(os.getcwd(), 'tests')  # name of directory under which test exists
    if test_name != "statFile":
        test_file = "test_" + test_name + ".py"
        test_file_path = os.path.join(os.path.join(directory_path, directory), test_file)
        if not os.path.exists(test_file_path):
            raise Exception(test_name + " test file does not exists")


def check_input_validity(params):
    # Checks the parameter type

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

    for test in tasks.values():
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


def docker_exec(container_name, arg, user=None, working_dir=None):
    run_script = "python3 run_container.py --test"
    if working_dir and user:
        cmd = "sudo docker exec -it -u %s -w %s %s %s %s" % (user, working_dir, container_name, run_script, arg)
    else:
        cmd = "sudo docker exec -it %s %s %s" % (container_name, run_script, arg)
    os.system(cmd)


def docker_cp_from_container(container_name, path, user=None):
    container_command = "docker cp %s%s" % (container_name, path)
    cmd = container_command + user + "/logs ." if user else container_command + "logs ."
    os.system(cmd)


def main():
    args = get_args()
    yaml_path = os.path.join(os.getcwd(), args.configfile)
    # container name
    container = "jupyter-" + args.session
    tasks = get_config(yaml_path)
    # Validates YAML File
    validator(tasks)

    if args.user_mode:
        if args.session == None:
            raise Exception("session argument needed")
        for test in args.test:
            if test == "storage":
                cp_helper(args.session, test, container)
                dir = "/scratch/" + args.session
                docker_exec(container, test, user=args.session, working_dir=dir)
                docker_cp_from_container(container, ":/scratch/", args.session)

            if test == "jupyterhub-api":
                cp_helper(args.session, test)
                container_name = "jupyterhub"
                docker_exec(container_name, test)
                docker_cp_from_container(container, ":/")

            if test == "CVMFS":
                cp_helper(args.session, test, container)
                docker_exec(container, test)
                docker_cp_from_container(container, ":/")

    else:
        # From host
        for test in args.test:
            if test == "storage":
                run_storage(tasks)

            if test == "jupyterhub-api":
                run_jupyterhub_api(tasks)

            if test == "CVMFS":
                run_cvmfs(tasks)


if __name__ == "__main__":
    main()
