import os


def docker_cp_from_container(container_name, path, user=None):
    """Copies log folders from container to host"""

    container_command = "docker cp %s%s" % (container_name, path)
    cmd = container_command + user + "/logs ." if user else container_command + "logs ."
    os.system(cmd)


def docker_cp_host(container_name, dest=""):
    """Copies files and folders to relevant containers"""

    file_list = ['run.py', 'test.yaml', 'run_container.py']
    folder_list = ['tests']
    for file in file_list:
        try:
            path_to_file = os.path.join(dest, file)
            path = "%s:%s" % (container_name, path_to_file)
            cmd = "docker cp %s %s" % (file, path)
            os.system(cmd)
        except Exception as exc:
            raise Exception
    for folder in folder_list:
        try:
            path_to_folder = os.path.join(dest, folder)
            path = "%s:%s" % (container_name, path_to_folder)
            cmd = "docker cp %s/. %s" % (folder, path)
            os.system(cmd)
        except Exception as exc:
            raise Exception
