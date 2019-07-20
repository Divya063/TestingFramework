import os
import glob
import sys
import subprocess
from test_check_api import  CheckAPI
from test_stop_session import StopSession
from test_create_session import CreateSession
from test_check_session import CheckSession


def run_jupyterhub_api(tasks):
    """Helper function for running Jupyterhub API test suite """

    test_jupyterhub = tasks['tests']['jupyterhub_api']

    # Check if API is reachable

    port = test_jupyterhub['check_api']['port']
    TLS = test_jupyterhub['check_api']['TLS']
    base_path = test_jupyterhub['check_api']['base_path']
    session_token = test_jupyterhub['create_session']['token']
    exit_code = 0
    test_reachable = CheckAPI(port, session_token, base_path, TLS)
    exit_code |= test_reachable.exit_code()
    if exit_code:
        raise Exception("API is not reachable..")
        sys.exit()

    # Check if session is created successfully

    session_port = test_jupyterhub['create_session']['port']
    session_users = test_jupyterhub['create_session']['users']
    session_params = test_jupyterhub['create_session']['params']
    session_base_path = test_jupyterhub['create_session']['base_path']
    session_delay = test_jupyterhub['create_session']['timedelay']
    session_TLS = test_jupyterhub['create_session']['TLS']
    test_create_session = CreateSession(session_port, session_token, session_users, session_params, session_delay, session_base_path, session_TLS)
    exit_code |= test_create_session.exit_code()

    # Check if the session is active

    session_port1 = test_jupyterhub['check_session']['port']
    session_users1 = test_jupyterhub['check_session']['users']
    session_TLS1 = test_jupyterhub['check_session']['TLS']
    session_base_path1 = test_jupyterhub['create_session']['base_path']
    test_active_session = CheckSession(session_port1, session_token, session_users1, session_base_path1, session_TLS1)
    exit_code |= test_active_session.exit_code()

    # Check if the session was stopped

    session_port2 = test_jupyterhub['stop_session']['port']
    session_users2 = test_jupyterhub['stop_session']['users']
    session_TLS2 = test_jupyterhub['stop_session']['TLS']
    session_base_path2 = test_jupyterhub['create_session']['base_path']
    test_stop_session = StopSession(session_port2, session_token, session_users2, session_base_path2, session_TLS2)
    exit_code |= test_stop_session.exit_code()

    return exit_code

