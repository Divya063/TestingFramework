import os
import time
import sqlite3
from sqlite3 import Error
import sys

sys.path.append("..")
from TestBase import Test
from logger import Logger


class DatabaseTest(Test):
    """Implements database connection"""

    def __init__(self, path, user, mode):
        super().__init__()
        self.path = path
        self.user = user
        self.mode = mode
        self.cur = None
        self.create_connection(path)

    def create_connection(self, path):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param path: path of database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(path)
        except Error as e:
            print(e)
        else:
            self.cur = conn.cursor()

    def select_tasks(self, command):
        """
        Query all rows in the tasks table
        :param command: Command to be exec
        :return: rows
        """

        try:
            self.cur.execute(command)
        except Exception as e:
            self.log.write("error", str(e))
        else:
            rows = self.cur.fetchall()
            return rows
