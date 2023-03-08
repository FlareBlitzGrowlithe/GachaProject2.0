import sqlite3
from flask import g


def connect_db(database):
    """
    Connect to the specified database.
    """
    conn = sqlite3.connect(database, check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def get_db(database):
    """
    Open a new database connection if there isn't one for the current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(database)
    return g.sqlite_db


def query_db(database, query, args=(), one=False):
    """
    Execute a database query and return the results.
    """
    conn, cursor = get_db(database)
    cursor.execute(query, args)
    results = cursor.fetchall()
    conn.close()
    return (results[0] if results else None) if one else results
