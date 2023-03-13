#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.database import connect_db
import random

def get_equipment_by_id(equipment_id):
    """
    Retrieve equipment data from equipment database by ID.
    """
    conn, cursor = connect_db('database/equipment.db')
    query = "SELECT * FROM equipment WHERE ids = ?"
    cursor.execute(query, (equipment_id,))
    result = cursor.fetchone()
    conn.close()
    return get_result(result)



def get_equipment_by_innerid(equipment_id, rarity):
    """
    Retrieve equipment data from equipment database by ID.
    """
    conn, cursor = connect_db('database/equipment.db')
    #query = "SELECT * FROM equipment WHERE innerid = ? AND rarity = ?"
    #cursor.execute(query, (equipment_id, rarity))
    cursor.execute("SELECT * FROM equipment WHERE innerid=? AND rarity=?",
              (equipment_id, rarity))

    result = cursor.fetchone()
    conn.close()
    return get_result(result)


def get_equipment_full_list():
    """
    Retrieve all equipment data from equipment database.
    """
    conn, cursor = connect_db('database/equipment.db')
    query = "SELECT * FROM equipment"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return [{
        "category": result[0],
        "name": result[1],
        "ids": result[2],
        "innerid": result[3],
        "rarity": result[4],
        "class": result[5],
        "cost": result[6],
        "stats": result[7],
        "effect": result[8],
        "notes": result[9]
    } for result in results]


def roll_equipment_by_rarity(rarity):
    """
    Retrieve equipment data from equipment database by rarity.
    """
    conn, cursor = connect_db('database/equipment.db')
    query = "SELECT * FROM equipment WHERE rarity = ?"
    #query = "SELECT COUNT(*) FROM equipment WHERE rarity = ?"

    cursor.execute(query, (rarity,))
    rows = cursor.fetchall()
    result = random.choice(rows)
    conn.close()

    return get_result(result)
    
def get_result(result):
    if result is None:
        return None
    else:
        return {
            "category": result[0],
            "name": result[1],
            "ids": result[2],
            "innerid": result[3],
            "rarity": result[4],
            "class": result[5],
            "cost": result[6],
            "stats": result[7],
            "effect": result[8],
            "notes": result[9]
        }


def add_equipment_to_pool(equipment):
    """
    Insert equipment data into equipment.db.
    """
    conn, cursor = connect_db('database/equipment.db')
    query = "INSERT INTO equipment (Name, Category, Ids, innerid, Rarity, Class, Cost, Stats, Effect, Notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, (equipment['name'], equipment['category'], equipment['ids'], equipment['innerid'], equipment['rarity'],
                   equipment['class'], equipment['cost'], equipment['stats'], equipment['effect'], equipment['notes']))
    conn.commit()
    conn.close()
