"""

Copies files and folders to relevant containers
"""
import subprocess
import os


def storage_user_container(name):
    try:
        cmd1 = "docker cp run.py "+ "jupyter-" + name + ":/scratch/" + name + "/run.py"
        os.system(cmd1)
        cmd2 = "docker cp test.yaml "+ "jupyter-"+ name + ":/scratch/" + name + "/test.yaml"
        os.system(cmd2)
        cmd3 = "docker cp tests/. " + "jupyter-" +name + ":/scratch/" + name+ "/tests"
        os.system(cmd3)
        cmd4 = "docker cp run_container.py " + "jupyter-" + name + ":/scratch/" + name + "/run_container.py"
        os.system(cmd4)
    except Exception as exc:
        raise Exception


def user_container(name):
    try:
        cmd1 = "docker cp run.py "+ "jupyter-" + name + ":/run.py"
        os.system(cmd1)
        cmd2 = "docker cp test.yaml "+ "jupyter-"+ name + ":/test.yaml"
        os.system(cmd2)
        cmd3 = "docker cp tests/. " + "jupyter-" +name + ":/tests"
        os.system(cmd3)
        cmd4 = "docker cp run_container.py " + "jupyter-" + name + ":/run_container.py"
        os.system(cmd4)
    except Exception as exc:
        raise Exception

def jupyterhub_container(name):
    try:
        cmd1 = "docker cp run.py "+ "jupyterhub" + ":/run.py"
        os.system(cmd1)
        cmd2 = "docker cp test.yaml "+ "jupyterhub" + ":/test.yaml"
        os.system(cmd2)
        cmd3 = "docker cp tests/. " + "jupyterhub" + ":/tests"
        os.system(cmd3)
        cmd4 = "docker cp run_container.py " + "jupyterhub" + ":/run_container.py"
        os.system(cmd4)
    except Exception as exc:
        raise Exception

