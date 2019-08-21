import argparse
from databasetest import DatabaseTest
import sys
sys.path.append("..")


def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("--path", dest="path",
                        required=True,
                        help='Specify the path of sqlite file')
    parser.add_argument("--user", dest="user",
                        required=True,
                        help='Specify the username for which session is running')
    parser.add_argument("--table", dest="table",
                        required=True,
                        help='Specify the table')
    parser.add_argument("-d", "--delete", action='store_true')
    parser.add_argument("-c", "--active", action='store_true')
    args = parser.parse_args()
    return args


class Servers(DatabaseTest):
    """
    Checks the status of "servers" table under two modes:
    1. When server of a particular user is active
    2. When server is removed or deleted

    Command :  python3 test_servers.py --path jupyterhub.sqlite -d --user user2 --table servers
    """

    def __init__(self, path, user, mode, table_name):
        self.ref_test_name = "test_servers"
        self.table_name = table_name
        super().__init__(path, user, mode)

    def run_test(self):
        command = 'select port, base_url from %s' % self.table_name
        result = self.select_tasks(command)
        # result format if mode is delete - []
        # format if mode is active - [(8888, '/user/user2/')]
        if len(result) == 0:
            self.log.write("info", "Server is not active, server table is empty")
            exit_code = 1 if self.mode else 0
        else:
            self.log.write("info", "Server is active, %s" % result)
            exit_code = 0 if self.mode else 1

        self.log.write("info", "exit code %s" % exit_code)
        return exit_code


if __name__ == "__main__":
    args = get_args()
    mode = 1 if args.active else 0 if args.delete else None
    test_servers = Servers(args.path, args.user, mode, args.table)
    test_servers.run_test()
