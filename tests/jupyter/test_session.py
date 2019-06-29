import json
import requests
import subprocess
import os
import argparse



def get_args():
    parser = argparse.ArgumentParser(description='Arguments', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--port", dest="port", type=int,
                        required = True,
                        )
    parser.add_argument( "--users", nargs='+', dest="users",
                        required  = True,
                        help='list of users')
    parser.add_argument("--path", dest="path",
                        required=True,
                        help = 'Path where config file exists')
    args = parser.parse_args()
    return args


class Session:
    def __init__(self, port, users, configfile):
        self.port = port
        self.users = users
        self.configfile = configfile
        self.main_url = "https://localhost:" + str(self.port) + "/hub/api/"
        self.exit = 0
        self.token = ""

    def check_create_token(self):
        os.chdir(self.configfile)
        command = subprocess.run(["jupyterhub", "token", "dummy_admin"], stdout=subprocess.PIPE)
        print(command.stdout.decode('utf-8').split("\n")[1])
        print(command.returncode)
        if command.returncode != 0:
            self.exit |= 1
            print(command.stdout.decode('utf-8'))
        else:
            self.token = command.stdout.decode('utf-8').split("\n")[1]

        return self.exit


    def check_create_users(self):

        """
        Inside container
        port = 443

        Ouside container
        port = 8443
        """
        for user in self.users:
            print(user)
            r = requests.post(self.main_url + 'users/%s' % user,
                              headers={
                                  'Authorization': 'token %s' % self.token,
                              },
                              verify=False
                              )
            print(r.status_code)
            if r.status_code == 201:
                print("successful")
            else:
                self.exit|=1
                r.raise_for_status()

        return self.exit

    def check_create_sessions(self):
        for user in self.users:
            print(user)
            data = { "LCG-rel":"LCG_95a", "platform": "x86_64-centos7-gcc7-opt", "scriptenv": "none", "ncores": 2, "memory": 8589934592, "spark-cluster": "none"}

            r = requests.post(self.main_url + 'users/%s' % user + "/server",
                              headers={
                                  'Authorization': 'token %s' % self.token,
                              },
                              json = data,
                              verify=False
                              )
            print(r.status_code)
            if r.status_code == 202:
                print("successful")
            else:
                self.exit |= 1
                r.raise_for_status()

        return self.exit


    def exit_code(self):
        self.exit |= self.check_create_token()
        self.exit |= self.check_create_users()
        self.exit|= self.check_create_sessions()
        return self.exit


if __name__ == "__main__":
    args = get_args()
    test_session = Session(args.port, args.users, args.path)
    print(test_session.exit_code())


