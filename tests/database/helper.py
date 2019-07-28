import os
import glob
from test_token import Tokens
from test_servers import Servers
from test_spawners import Spawners


def run_database(tasks):
    """
     Helper function for running database test suite
    """
    test_database = tasks['tests']['database']
    file_path = test_database['path']
    # Tokens table
    user = test_database['token']['user']
    table = test_database['token']['table']
    mode = test_database['token']['mode']
    exit_code = 0
    test_tokens = Tokens(file_path, user, mode, table)
    exit_code |= test_tokens.exit_code()

    # servers table
    user = test_database['servers']['user']
    table = test_database['servers']['table']
    mode = test_database['servers']['mode']
    exit_code = 0
    test_servers = Servers(file_path, user, mode, table)
    exit_code |= test_servers.exit_code()

    # spawners table
    user = test_database['spawners']['user']
    table = test_database['spawners']['table']
    mode = test_database['spawners']['mode']
    exit_code = 0
    test_spawners = Spawners(file_path, user, mode, table)
    exit_code |= test_spawners.exit_code()

    return exit_code
