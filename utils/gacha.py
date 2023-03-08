#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from utils.user import update_user_gold
from utils.equipment import roll_equipment_by_rarity

success_level_probs = {
    "minion": [[30, 29, 26, 20], [30, 29, 28, 22], [30, 30, 29, 24], 
               [30, 30, 30, 26], [30, 30, 30, 30]],
    "boss": [[29, 26, 22, 15], [29, 28, 25, 18], [30, 29, 26, 20], 
             [30, 30, 28, 23], [30, 30, 30, 28]]
}
luck_label = ["大成功", "极难成功", "困难成功", "成功", "失败", "大失败"]
pool_price={"minion":7, "boss":10}

def draw_gacha(pool, user, times=1):
    user_luck = user['luck']
    results = []
    for i in range(times):
        success_level, roll = roll_success_level(user_luck)
        if success_level>4:
            continue
        rarity = roll_rarity(pool, success_level)
        equipment = roll_equipment(rarity)
        equipment['success_level'] = luck_label[success_level]
        equipment['roll'] = roll
        equipment['pool'] = pool
        results.append(equipment)
    update_user_gold(user["user_id"], user["gold"]-pool_price[pool]*times)
    return [results, user["gold"]-pool_price[pool]*times]


def roll_success_level(user_luck):
    roll = random.randint(1, 100)
    if roll > user_luck and roll > 95:
        return [5,roll]
    elif roll > user_luck and roll <= 95:
        return [4, roll]
    elif roll < user_luck/4:
        return [1, roll]
    elif roll < user_luck/2:
        return [2, roll]
    elif roll < user_luck and roll<=5:
        return [0, roll]
    else:
        return [3, roll]


def roll_rarity(pool, success_level):
    roll = random.randint(0, 30)
    Rare = success_level_probs[pool][success_level]
    if roll > Rare[0]:
        prob = "神"
    elif roll > Rare[1]:
        prob = "圣"
    elif roll > Rare[2]:
        prob = "皇"
    elif roll > Rare[3]:
        prob = "贤"
    else:
        prob = "凡"
    return prob


def roll_equipment(rarity):

    #equipment_id = random.randint(1, get_equipment_count_by_rarity(rarity))
    # get equipment by rarity from equipment.py
    # assuming get_equipment_by_rarity() is defined in equipment.py

    return roll_equipment_by_rarity(rarity)
