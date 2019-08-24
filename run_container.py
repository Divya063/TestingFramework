import argparse
import glob
import os
import sys
import yaml
import subprocess
import importlib


# run tests from user container

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        nargs='*', default='compTest',
                        required=True,
                        help='name of the test you want to run')
    args = parser.parse_args()
    return args


def get_config(cfg):
    if os.path.exists(cfg):
        with open(cfg, 'r') as stream:
            return yaml.safe_load(stream)
    else:
        raise Exception("yaml file not present")


def install_requirements():
    command = "pip3 install -r requirements.txt"
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()


def run_tests(tasks, test_name):
    test_num = 0
    test_passed = 0
    ignore_params = ['statFile']
    passed = []
    install_requirements()
    for key, value in tasks.items():
        # skip output parameters present in yaml
        if key == "output":
            continue
        for directory, test in value.items():
            if directory == test_name:
                if test:
                    for test_name, param in test.items():
                        if test_name in ignore_params:
                            continue
                        class_name = ""
                        test_num = test_num + 1
                        string_list = test_name.split("_")
                        for string in string_list:
                            class_name += string.capitalize()
                        test_name = "test_%s" % test_name
                        module_name = 'tests.%s.%s' % (directory, test_name)
                        # Dynamically import the class name
                        module = importlib.import_module(module_name)
                        class_ = getattr(module, class_name)
                        instance = class_(**param)
                        exit_code = instance.run_test()
                        if exit_code == 0:
                            passed.append(directory + "_" + test_name)
                            test_passed = test_passed + 1

    print("Total tests passed %s" % test_passed, " | Total number of tests %s" % test_num)
    print("List of the tests passed", passed)


def main():
    tasks = get_config('test.yaml')
    args = get_args()
    run_tests(tasks, args.test[0])


if __name__ == "__main__":
    main()
