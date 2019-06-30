import os
import glob
import sys
from test_webReachable import webReachable
from test_stop_session import StopSession
from test_session import Session
from test_active_session import ActiveSession



def run_jupyterhub_api(tasks):
    """
     Helper function for running Jupyterhub API test suite
    """
    test_jupyterhub = tasks['tests']['jupyterhub_api']
    """
    check if API is reachable
    """
    port = test_jupyterhub['webReachable']['port']
    exit_code = 0
    test_reachable = webReachable(port)
    exit_code |= test_reachable.exit_code()
    if(exit_code):
        raise Exception("API is not reachable..")
        sys.exit()

    """
    check if session is created successfully
    """
    session_port = test_jupyterhub['session']['port']
    session_users = test_jupyterhub['session']['users']
    session_path = test_jupyterhub['session']['path']
    test_session = Session(session_port, session_users, session_path)
    exit_code |= test_session.exit_code()
    """
    Check if the session is active
    """
    session_port1 = test_jupyterhub['active_session']['port']
    session_users1 = test_jupyterhub['active_session']['users']
    session_path1 = test_jupyterhub['active_session']['path']
    test_active_session = ActiveSession(session_port1, session_users1, session_path1)
    exit_code |= test_active_session.exit_code()
    """
    Check if the session was stopped
    """
    session_port2 = test_jupyterhub['stop_session']['port']
    session_users2 = test_jupyterhub['stop_session']['users']
    session_path2 = test_jupyterhub['stop_session']['path']
    test_stop_session = StopSession(session_port2, session_users2, session_path2)
    exit_code |= test_stop_session.exit_code()

    return exit_code

