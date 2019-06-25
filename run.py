import argparse
import glob
import os
import sys
import yaml

from tests.storage.helper import run_storage

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        nargs='*', default='compTest',
                        required=False,
                        help='name of the test you want to run')
    parser.add_argument('-c', '--configfile',
                        required = True,
                        help='load config file')
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
    """
    Checks if mentioned tests exist in particular directory or not
    """
    directory_path = os.path.join(os.getcwd(), 'tests') #name of directory under which test exists
    if(test_name!= "statFile"):
        test_file = "test_" + test_name + ".py"
        test_file_path = os.path.join(os.path.join(directory_path, directory), test_file)
        if not os.path.exists(test_file_path):
            raise Exception( test_name + " test file does not exists")

def check_input_validity(params):
    """
    Check the parameter type
    """
    string_val = ['filePath', 'fileSize','repoName', 'repoSize']
    int_val = ['fileNumber', 'num']
    for key, value in params.items():
        if key in int_val:
            if not type(value) == int:
                raise Exception(key + " having value " + str(value)+ " is not integer")
        if key in string_val:
            if not type(value)==str:
                raise Exception( key + " having value" + str(value) + " is not string")




def validator(tasks):
    """
    To check validity of YAML File
    """
    for test in tasks.values():
        for directory, component_test in test.items(): #storage
            if(component_test!=None):
                for test_name, param in component_test.items():
                    if(param!=None):
                        check_test_exists(directory, test_name)
                        check_input_validity(param)



def cleanup():
    """
    delete the created files
    """
    filelist = glob.glob(os.path.join("", "*.txt"))
    print(filelist)
    for f in filelist:
        os.remove(f)

def main():
    args = get_args()
    yaml_path= os.path.join(os.getcwd(), args.configfile)
    tasks = get_config(yaml_path)
   # Validates YAML File
    validator(tasks)
    for test in args.test:
        if test == "storage":
            #passes the parameters loaded from yaml file to helper function
            run_storage(tasks)
            cleanup()

if __name__ == "__main__":
    main()
