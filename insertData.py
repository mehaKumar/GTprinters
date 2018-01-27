import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def create_issue(conn, issue):
    """
    Create a new issue into the tickets table
    :param conn:
    :param issue:
    :return: issue id
    """
    sql =  "INSERT INTO tickets(timestamp, printer, issue)" + "VALUES(?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, issue)
    return cur.lastrowid

def main():
    database = "Printer_Data.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new issue
        issue = (20180127, 'Klaus printer', 'out of paper');
        issue_id = create_issue(conn, issue)

if __name__ == '__main__':
    main()