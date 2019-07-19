import os
import glob
from test_mount_sanity import MountSanity
from test_mount import Mount
from test_throughput import Throughput
from test_checksum import Checksum
from test_write import Write
from test_exists import Exists
from test_delete import Delete




def run_storage(tasks):
    """
     Helper function for running storage test suite
    """
    exit_code = 0

    test_storage = tasks['tests']['storage']
    time = test_storage['mount_sanity']['timeout']
    mount_points = test_storage['mount_sanity']['mountpoints']
    test_mount_sanity = MountSanity(time, mount_points)
    try:
        exit_code |= test_mount_sanity.exit_code()
    except Exception as err:
        print(err)

    test_mount = Mount()
    exit_code |= test_mount.exit_code()

    file_path = test_storage['statFile']['filepath']
    number_of_files = test_storage['throughput']['fileNumber']
    size = test_storage['throughput']['fileSize']

    test_io = Throughput(number_of_files, size, file_path)
    exit_code |= test_io.exit_code()
    number_of_files = test_storage['checksum']['fileNumber']
    size = test_storage['checksum']['fileSize']
    test_integrity= Checksum(number_of_files, size, file_path)
    exit_code |= test_integrity.exit_code()

    file_size = test_storage['write']['fileSize']
    test_write = Write(file_size, file_path)
    exit_code |= test_write.exit_code()

    file_name = test_storage['delete']['fileName']
    test_delete = Delete(file_name, file_path)
    exit_code |= test_delete.exit_code()

    file_name1 = test_storage['exists']['fileName']
    test_exists = Exists(file_name1, file_path)
    exit_code |= test_exists.exit_code()

    return exit_code

