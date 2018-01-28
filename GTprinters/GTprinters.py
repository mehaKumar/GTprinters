# all the imports
import os
import sqlite3
from sqlite3 import Error
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'Printer_Data.db'),
    SECRET_KEY='sossecret'
))
app.config.from_envvar('GTPRINTERS_SETTINGS', silent=True)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(e)

    return None

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = create_connection("/home/mkumar77/GTprinters/Printer_Data.db")
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select * from tickets order by timestamp desc')
    tickets = cur.fetchall()
    return render_template('index.html', tickets=tickets)

@app.route('/issue')
def show_issue():
    return render_template('issue.html')

@app.route('/add_entry', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute("INSERT INTO tickets(timestamp, printer, issue) " + "VALUES(?,?,?)",
                 [request.form['timestamp'], request.form['printer'], request.form['issue']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

if __name__ == "__main__":
    app.run()