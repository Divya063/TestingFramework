import argparse
import logging
import yaml
import glob
import os
from EOS.helper import run_eos


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        nargs='*', default='compTest',
                        required=False,
                        help='name of the test you want to run')
    parser.add_argument('-j', '--json',
                        required=False,
                        action='store',
                        help='Output to json file')
    args = parser.parse_args()
    return args


def get_config(cfg):
    with open(cfg, 'r') as stream:
        return yaml.safe_load(stream)

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
    logging.basicConfig(level=logging.INFO, filename='test.log', filemode='w',
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logging.info('Started')
    logger = logging.getLogger(args.test[0])
    tasks = get_config('test.yaml')
    for test in args.test:
        if test == "EOS":
            run_eos(tasks)
            cleanup()
    logging.info('Finished')

if __name__ == "__main__":
    main()
