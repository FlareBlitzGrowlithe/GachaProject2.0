#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.database import connect_db
from utils.user import *
from utils.equipment import get_equipment_by_id
import datetime

PRICE_CHART_SELLING = {"神": 20, "圣": 10, "皇": 8, "贤": 5, "凡": 3 }

# add a new equipment to the user's inventory with current timestamp.
def add_equipment_to_userid(equipment):
    conn, cursor = connect_db('database/inventory.db')
    query = "INSERT INTO inventory (user_id, pool, success_level, roll, equipment_id, timestamp) VALUES (?, ?, ?, ?, ?, ?)"
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(query, (equipment["user_id"], equipment["pool"],
                   equipment["success_level"], equipment["roll"], equipment["equipment_id"], timestamp))
    conn.commit()
    conn.close()

# remove an equipment from the user's inventory by ID.
def remove_equipment_from_inventory(user_id, equipment_id):
    conn, cursor = connect_db('database/inventory.db')
    query = "DELETE FROM inventory WHERE ROWID IN(SELECT ROWID FROM inventory WHERE user_id= ? AND equipment_id= ? LIMIT 1)"
    cursor.execute(query, (user_id, equipment_id))
    conn.commit()
    conn.close()

# remove an equipment from the user's inventory and add its value to the user's gold.
def sell_equipment(user, equipment_id):
    equipment = get_equipment_by_id(equipment_id)
    user_id = user['user_id']
    user = get_user_by_id(user_id)
    if equipment is None:
        return False
    else:
        if user is None:
            return False
        else:
            update_user_gold(
                user_id, user['gold']+PRICE_CHART_SELLING[equipment['rarity']])
            remove_equipment_from_inventory(user_id, equipment_id)
            return True
        
# retrieve all equipment data from inventory database for the specified user.
def get_equipment_by_userid(user_id):
    conn, cursor = connect_db('database/inventory.db')
    query = "SELECT * FROM inventory WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    results = cursor.fetchall()
    conn.close()
    return [{
        "user_id": result[0],
        "pool": result[1],
        "success_level": result[2],
        "roll": result[3],
        "equipment_id": result[4],
        "equipment": get_equipment_by_id(result[4]),
        "timestamp":result[5]
    } for result in results]

# retrieve all equipment data from inventory database.

def get_inventory_full_list():
    conn, cursor = connect_db('database/inventory.db')
    query = "SELECT * FROM inventory"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [{
        "user_id": result[0],
        "pool": result[1],
        "success_level": result[2],
        "roll": result[3],
        "equipment_id": result[4],
        "equipment": get_equipment_by_id(result[4]),
        "timestamp":result[5]

    } for result in results]
