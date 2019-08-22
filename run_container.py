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


def run_tests(tasks, test_name):
    ignore_params = ['statFile']
    for key, value in tasks.items():
        # skip output parameters present in yaml
        if key == "output":
            continue
        for directory, test in value.items():
            print(directory)
            if directory == test_name:
                if test:
                    for test_name, param in test.items():
                        print(test_name, param)
                        if test_name in ignore_params:
                            continue
                        class_name = ""
                        string_list = test_name.split("_")
                        for string in string_list:
                            print(class_name)
                            class_name += string.capitalize()
                        test_name = "test_%s" % test_name
                        module_name = 'tests.%s.%s' % (directory, test_name)
                        # Dynamically import the class name
                        module = importlib.import_module(module_name)
                        class_ = getattr(module, class_name)
                        instance = class_(**param)
                        instance.run_test()
            else:
                break


def main():
    tasks = get_config('test.yaml')
    args = get_args()
    run_tests(tasks, args.test[0])


if __name__ == "__main__":
    main()
