import os
import glob
import sys
from test_check_api import  CheckAPI
from test_stop_session import StopSession
from test_create_session import CreateSession
from test_check_session import CheckSession



def run_jupyterhub_api(tasks):
    """
     Helper function for running Jupyterhub API test suite
    """
    test_jupyterhub = tasks['tests']['jupyterhub_api']
    """
    check if API is reachable
    """
    port = test_jupyterhub['check_api']['port']
    exit_code = 0
    test_reachable = CheckAPI(port)
    exit_code |= test_reachable.exit_code()
    if(exit_code):
        raise Exception("API is not reachable..")
        sys.exit()

    """
    check if session is created successfully
    """
    session_port = test_jupyterhub['create_session']['port']
    session_users = test_jupyterhub['create_session']['users']
    session_token = test_jupyterhub['create_session']['token']
    session_params= test_jupyterhub['create_session']['params']
    test_create_session = CreateSession(session_port, session_users, session_token, session_params)
    exit_code |= test_create_session.exit_code()
    """
    Check if the session is active
    """
    session_port1 = test_jupyterhub['check_session']['port']
    session_users1 = test_jupyterhub['check_session']['users']
    session_token1 = test_jupyterhub['check_session']['token']
    test_active_session = CheckSession(session_port1, session_users1, session_token1)
    exit_code |= test_active_session.exit_code()
    """
    Check if the session was stopped
    """
    session_port2 = test_jupyterhub['stop_session']['port']
    session_users2 = test_jupyterhub['stop_session']['users']
    session_token2 = test_jupyterhub['stop_session']['token']
    test_stop_session = StopSession(session_port2, session_users2, session_token2)
    exit_code |= test_stop_session.exit_code()

    return exit_code

