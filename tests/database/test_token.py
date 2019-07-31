import argparse
import sys
sys.path.append("..")
from databasetest import DatabaseTest


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


class Token(DatabaseTest):
    """
    Checks the status of "api_tokens" table under two modes:
    1. When server of a particular user is active
    2. When server is removed or deleted

    Command :  python3 test_token.py --path jupyterhub.sqlite -d --user user2 --table api_tokens
    """

    def __init__(self, path, user, mode, table_name):
        self.ref_test_name = "test_token"
        self.table_name = table_name
        super().__init__(path, user, mode)

    def check_token(self):
        command = 'select user_id, note from %s' % self.table_name
        result = self.select_tasks(command)
        # result format if mode is delete - [(None, 'generated at startup')]
        # format if mode is active - [(1, 'Server at /user/user2/')]
        user_id = result[0][0]
        server = result[0][1]
        if user_id:
            self.log.write("info", "Server is active")
            server_address = 'Server at user/%s' % self.user
            if server == server_address:
                self.log.write("info", server_address)
                self.exit = 0 if self.mode else 1
        else:
            self.exit = 1 if self.mode else 0

        return self.exit

    def exit_code(self):
        self.exit = self.check_token()
        self.log.write("info", "exit code %s" % self.exit)
        return self.exit


if __name__ == "__main__":
    args = get_args()
    mode = 1 if args.active else 0 if args.delete else None
    test_token = Token(args.path, args.user, mode, args.table)
    test_token.exit_code()
