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
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--test',
                        nargs='*', default='compTest',
                        required=False,
                        help='name of the test you want to run')
    parser.add_argument('-c', '--configfile',
                        required = False,
                        help='load config file')

    parser.add_argument("-u", "--user_mode", action='store_true')

    parser.add_argument('-s', '--session',
                        required=False,
                        help= 'session name')

    parser.add_argument('-p', '--path',
                        required= False,
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

def container_name(username):
    name = "jupyter-" + username
    return name

def docker_exec(container_name,  arg, user = None, working_dir=None):
    if(working_dir != None and user != None):
        cmd = "sudo docker exec -it " + "-u "+ user+ " -w "+ working_dir + " "+ container_name + " python3 run_container.py --test " + arg
    else:
        cmd = "sudo docker exec -it " + container_name + " python3 run_container.py --test "+ arg
    os.system(cmd)




def docker_cp_container(container_name, path, user = None):
    if(user!=None):
        cmd = "docker cp " + container_name + path + user + "/logs ."
    else:
        cmd = "docker cp " + container_name + path + "logs ."
    os.system(cmd)





def main():
    args = get_args()
    yaml_path= os.path.join(os.getcwd(), args.configfile)
    tasks = get_config(yaml_path)
   # Validates YAML File
    validator(tasks)

    if (args.user_mode):
        if(args.session == None):
            raise Exception("session argument needed")
        for test in args.test:
            if test == "storage":
                cp_helper(args.session, test)
                dir = "/scratch/" + args.session
                container = container_name(args.session)
                docker_exec(container, test, user= args.session, working_dir= dir)
                docker_cp_container(container, ":/scratch/", args.session)


            if test == "jupyterhub-api":
                cp_helper(args.session, test)
                container = "jupyterhub"
                docker_exec(container, test)
                docker_cp_container(container, ":/")


            if test == "CVMFS":
                cp_helper(args.session, test)
                container =  container_name(args.session)
                docker_exec(container, test)
                docker_cp_container(container, ":/")

    else:
        #From host
        for test in args.test:
            if test == "storage":
                run_storage(tasks)

            if test == "jupyterhub-api":
                run_jupyterhub_api(tasks)

            if test == "CVMFS":
                run_cvmfs(tasks)


if __name__ == "__main__":
    main()
