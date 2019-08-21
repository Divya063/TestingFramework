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


class Spawners(DatabaseTest):
    """
    Checks the status of "servers" table under two modes:
    1. When server of a particular user is active
    2. When server is removed or deleted

    Command :  python3 test_spawners.py --path jupyterhub.sqlite -d --user user2 --table spawners
    """

    def __init__(self, path, user, mode, table_name):
        self.ref_test_name = "test_spawners"
        self.table_name = table_name
        super().__init__(path, user, mode)

    def run_test(self):
        exit_code = 0
        command = 'select server_id from %s' % self.table_name
        result = self.select_tasks(command)
        # result format if mode is delete - [(None,)]
        # format if mode is active - [(1,)]
        if result:
            self.log.write("info", "Server is active, %s" % result)
            exit_code = 0 if self.mode else 1
        else:
            self.log.write("info", "Server is not active, server_id field is none")
            exit_code = 1 if self.mode else 0
        self.log.write("info", "exit code %s" % exit_code)
        return exit_code


if __name__ == "__main__":
    args = get_args()
    mode = 1 if args.active else 0 if args.delete else None
    test_spawners = Spawners(args.path, args.user, mode, args.table)
    test_spawners.run_test()
