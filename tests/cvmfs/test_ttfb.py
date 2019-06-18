
import argparse
import os
import time
from tests.logger import Logger, LOG_FOLDER, LOG_EXTENSION
from test_mount import check_mount

def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--repo", dest="repo_name",
                        required=True,
                        help='Repository name')

    parser.add_argument("--path", dest="file_path",
                        required=True,
                        help='Specify the path (file included)')

    args = parser.parse_args()
    return args

class TTFB:
    def __init__(self, repo, path):
        self.repo = repo
        self.path = path
        self.exit = None
        self.check_mount = check_mount(path)
        self.ref_test_name = "Time_till_First_Byte"
        self.logger_folder = os.path.join(os.getcwd(), LOG_FOLDER)
        self.log = Logger(os.path.join(self.logger_folder, self.ref_test_name + LOG_EXTENSION))
        self.log.write("info", "Tests starting...")
        self.log.write("info", time.strftime("%c"))
        self.exit = None
        self.ref_timestamp = int(time.time())
        self.log_params()

    def log_params(self):
        self.log.write("parameters", "Test name: " + self.ref_test_name)
        self.log.write("parameters", "Test time: " + str(self.ref_timestamp))


    def ttfb(self, path):
        global ttfb
        if(check_mount == 0):
            start = time.time()
            try:
                with open(path, 'rb') as file:
                    # read one byte
                    file.read(1)
                    ttfb = time.time() - start
            except Exception as err:
                self.log.write("error", "Error while reading " + path)
                self.log.write("error", path + ": " + str(err))
                self.exit |= 1

            else:
                self.log.write("Performance", "\t".join(
                    [path,  str(("%.8f" % float(ttfb)))]))
        else:
            self.log.write("error", "repository is not mounted")
            self.exit |= 1

        return self.exit

        def exit_code(self):
            code = self.ttfb(self.path)
            self.log.write("info", "exit code: " + str(self.exit))
            return code

if __name__ == "__main__":
    args = get_args()
    test_ttfb = ttfb(args.repo_name, args.path)
    test_ttfb.exit_code()


            








