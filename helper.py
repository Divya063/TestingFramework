# Copies files and folders to relevant containers

import subprocess
import os


def cp_helper(name, test_name):
    container_name = "jupyter-" + name
    if test_name == "storage":
        dest = "scratch/" + name + "/"
        docker_cp_host(container_name, dest)
    elif test_name == "jupyterhub-api":
        container_name = "jupyterhub"
        docker_cp_host(container_name, "")
    else:
        docker_cp_host(container_name, "")


def docker_cp_host(container_name, dest):
    file_list = ['run.py', 'test.yaml', 'run_container.py']
    folder_list = ['tests']
    for file in file_list:
        try:
            cmd = "docker cp %s %s:/%s%s" % (file, container_name, dest, file)
            os.system(cmd)
        except Exception as exc:
            raise Exception
    for folder in folder_list:
        try:
            cmd = "docker cp %s/. %s:/%s%s" % (folder, container_name, dest, folder)
            os.system(cmd)
        except Exception as exc:
            raise Exception
