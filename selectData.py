import sqlite3
from sqlite3 import Error
import datetime


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def select_all_issues(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tickets")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_recent_issues(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    dateCutoff = (datetime.datetime.now() - datetime.timedelta(seconds = 10))
    dateCutoff = dateCutoff.strftime("%Y%m%d%H%M%S")
    cur.execute("SELECT * FROM tickets WHERE timestamp > "+ dateCutoff)

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    database = "Printer_Data.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query issues by data (recent ones only):")
        select_recent_issues(conn)

        print("2. Query all tasks")
        select_all_issues(conn)


if __name__ == '__main__':
    main()