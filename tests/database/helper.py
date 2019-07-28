import os
import glob
from test_token import Token
from test_servers import Servers
from test_spawners import Spawners


def run_database(tasks):
    """
     Helper function for running database test suite
    """
    test_database = tasks['tests']['database']

    # Tokens table
    user = test_database['token']['user']
    table = test_database['token']['table']
    mode = test_database['token']['mode']
    file_path = test_database['token']['path']
    exit_code = 0
    test_tokens = Token(file_path, user, mode, table)
    exit_code |= test_tokens.exit_code()

    # servers table
    user = test_database['servers']['user']
    table = test_database['servers']['table']
    mode = test_database['servers']['mode']
    file_path = test_database['servers']['path']
    test_servers = Servers(file_path, user, mode, table)
    exit_code |= test_servers.exit_code()

    # spawners table
    user = test_database['spawners']['user']
    table = test_database['spawners']['table']
    mode = test_database['spawners']['mode']
    file_path = test_database['spawners']['path']
    test_spawners = Spawners(file_path, user, mode, table)
    exit_code |= test_spawners.exit_code()

    return exit_code
