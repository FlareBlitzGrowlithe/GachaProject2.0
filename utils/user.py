#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.database import connect_db

def add_user(user):
    """
    Add a new user to the user database.
    """
    conn, cursor = connect_db('database/user.db')
    query = "INSERT INTO user (username, password, admin, gold, luck) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (user["username"], user["password"],
                   user["admin"], user["gold"], user["luck"]))
    conn.commit()
    conn.close()


def delete_user(user_id):
    """
    Delete a user from the user database by ID.
    """
    conn, cursor = connect_db('database/user.db')
    query = "DELETE FROM user WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    conn.commit()
    conn.close()


def login(username, password):
    """
    Check if the username and password match in the user database.
    """
    conn, cursor = connect_db('database/user.db')
    query = "SELECT * FROM user WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return None
    else:
        return {
            "user_id": result[0],
            "username": result[1],
            "admin": bool(result[3]),
            "gold": result[4],
            "luck": result[5]
        }


def get_user_by_id(user_id):
    """
    Retrieve user data from user database by ID.
    """
    conn, cursor = connect_db('database/user.db')
    query = "SELECT * FROM user WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return None
    else:
        return {
            "user_id": result[0],
            "username": result[1],
            "admin": bool(result[3]),
            "gold": result[4],
            "luck": result[5]
        }


def get_user_by_username(username):
    """
    Retrieve user data from user database by username.
    """
    conn, cursor = connect_db('database/user.db')
    query = "SELECT * FROM user WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return None
    else:
        return {
            "user_id": result[0],
            "username": result[1],
            "password": result[2],
            "admin": bool(result[3]),
            "gold": result[4],
            "luck": result[5]
        }


def get_user_all():
    """
    Retrieve all user data from user database.
    """
    conn, cursor = connect_db('database/user.db')
    query = "SELECT * FROM user"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [{
        "user_id": result[0],
        "username": result[1],
        "admin": bool(result[3]),
        "gold": result[4],
        "luck": result[5]
    } for result in results]


def update_user(user):
    """
    Update a user's data in the user database.
    """
    conn, cursor = connect_db('database/user.db')
    query = "UPDATE user SET username = ?, password = ?, admin = ?, gold = ?, luck = ? WHERE user_id = ?"
    cursor.execute(query, (user["username"], user["password"],
                   user["admin"], user["gold"], user["luck"], user["user_id"]))
    conn.commit()
    conn.close()


def get_users_by_admin(admin):
    """
    Retrieve user data from user database by admin status.
    """
    conn, cursor = connect_db('database/user.db')
    query = "SELECT * FROM user WHERE admin = ?"
    cursor.execute(query, (admin,))
    results = cursor.fetchall()
    conn.close()
    return [{
        "user_id": result[0],
        "username": result[1],
        "admin": bool(result[3]),
        "gold": result[4],
        "luck": result[5]
    } for result in results]


def update_user_luck(user_id, luck):
    """
    Update a user's luck parameter in the user database.
    """
    conn, cursor = connect_db('database/user.db')
    query = "UPDATE user SET luck = ? WHERE user_id = ?"
    cursor.execute(query, (luck, user_id))
    conn.commit()
    conn.close()


def update_user_gold(user_id, gold):
    """
    Update a user's gold parameter in the user database.
    """
    conn, cursor = connect_db('database/user.db')
    query = "UPDATE user SET gold = ? WHERE user_id = ?"
    cursor.execute(query, (gold, user_id))
    conn.commit()
    conn.close()
