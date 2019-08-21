import argparse
import glob
import os
import sys
import yaml
import importlib
import subprocess

from helper import docker_cp_to_container, docker_cp_from_container, docker_exec



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
    """Checks if mentioned tests exist in particular directory or not"""
    lists = ["statFile"]
    directory_path = os.path.join(os.getcwd(), 'tests')  # name of directory under which test exists
    if test_name not in lists:
        test_file = "test_" + test_name + ".py"
        test_file_path = os.path.join(os.path.join(directory_path, directory), test_file)
        if not os.path.exists(test_file_path):
            raise Exception(test_name + " test file does not exists")


def check_input_validity(params):
    # Checks the parameter type

    string_val = ['filePath', 'fileSize', 'repoName', 'repoSize', 'repoPath', 'user', 'table', 'path', 'hostname',
                  'port', 'hostname', 'base_path', 'token', 'LCG-rel', 'platform', 'scriptenv', 'spark-cluster',
                  'container_name']
    int_val = ['fileNumber', 'num', 'timeout', 'num', 'mode', 'ncores', 'memory']
    list_type = ['mountpoints', 'users']
    bool_type = ['TLS']

    for key, value in params.items():
        if key in int_val:
            if not type(value) == int:
                raise Exception(key + " having value %s is not a integer" % str(value))
        elif key in string_val:
            if not type(value) == str:
                raise Exception(key + " having value %s is not a string" % str(value))

        elif key in list_type:
            if not type(value) == list:
                raise Exception(key + " having value %s is not a list" % str(value))

        elif key in bool_type:
            if not type(value) == bool:
                raise Exception(key + " having value %s is not a boolean value" % str(value))


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


def run_tests(tasks):
    ignore_params = ['statFile']
    for key, value in tasks.items():
        # skip output parameters present in yaml
        if key == "output":
            continue
        for directory, test in value.items():
            print(directory, test)
            if test:
                for test_name, param in test.items():
                    if test_name in ignore_params:
                        continue
                    class_name = ""
                    string_list = test_name.split("_")
                    for string in string_list:
                        class_name += string.capitalize()
                    test_name = "test_%s" % test_name
                    module_name = 'tests.%s.%s' % (directory, test_name)
                    # Dynamically import the class name
                    module = importlib.import_module(module_name)
                    class_ = getattr(module, class_name)
                    instance = class_(**param)
                    instance.run_test()


def main():
    args = get_args()
    yaml_path = os.path.join(os.getcwd(), args.configfile)
    tasks = get_config(yaml_path)
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
        run_tests(tasks)


if __name__ == "__main__":
    main()
