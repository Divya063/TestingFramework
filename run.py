import argparse
import glob
import os
import sys
import yaml

from tests.storage.helper import run_eos

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
    for test in args.test:
        if test == "EOS":
            #passes the parameters loaded from yaml file to helper function
            run_eos(tasks)
            cleanup()

if __name__ == "__main__":
    main()
