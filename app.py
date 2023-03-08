#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import make_response
from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from utils.user import *
from utils.gacha import *
from utils.equipment import *
from utils.inventory import *


app = Flask(__name__)
app.secret_key = 'my_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'Oceanic_Operetta_is_the_best!'


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/draw')
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    admin = False
    gold = 0
    luck = 50
    user = {"username": username, "password": generate_password_hash(
        password), "admin": admin, "gold": gold, "luck": luck}
    add_user(user)
    return redirect('/login')

# page /login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect('/user')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username)

        if user and check_password_hash(user["password"], password):
            session['user_id'] = user["user_id"]
            session['admin'] = user['admin']
            session.permanent = True
            response = redirect('/draw')
            response = set_username_cookie(response, username)
            return response
        else:
            return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')

# page /user
@app.route('/user')
def user():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    inventory = get_equipment_by_userid(user["user_id"])
    return render_template('user.html', user=user, inventory=inventory)

# page /draw
@app.route('/draw')
def draw():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    inventory = get_equipment_by_userid(user["user_id"])
    username = get_username_cookie(request)
    return render_template('draw.html', user=user, inventory=inventory, username=username)

# TODO: page /store 
@app.route('/store')
def store():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    inventory = get_equipment_by_userid(user["user_id"])
    return render_template('store.html', user=user, inventory=inventory)

# page admin control
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    inventory = get_equipment_by_userid(user["user_id"])
    return render_template('admin.html', user=user, inventory=inventory)

@app.route('/getinventoryall')
def get_inventory_all():
    if 'user_id' not in session:
        return redirect('/login')
    inventory = get_inventory_full_list()
    return jsonify(inventory=inventory)


@app.route('/getinventory')
def get_inventory():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    inventory = get_equipment_by_userid(user["user_id"])
    return jsonify(inventory=inventory)

@app.route('/getgold')
def get_gold():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    gold = user ["gold"]
    return jsonify(gold=gold)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

#gacha function
@app.route('/gacha', methods=['POST'])
def gacha():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    pool = request.form.get('pool')
    times = int(request.form.get('times'))
    [results, gold_left] = draw_gacha(pool, user, times)
    for result in results:
        if result!=[]:
            add_equipment({"user_id": user["user_id"], "pool": pool,
                     "success_level": result['success_level'], 
                     "roll": result['roll'],
                     "equipment_id": result['ids']})
    return jsonify(results=results, gold=gold_left)


@app.route('/sell', methods=['POST'])
def sell():
    if 'user_id' not in session:
        return redirect('/login')
    user = get_user_by_id(session['user_id'])
    equipment_id = request.form.get('equipment_id')
    sold = sell_equipment(user, equipment_id)
    if sold:
        inventory = get_equipment_by_userid(user["user_id"])
    return jsonify(inventory=inventory)


@app.route('/remove', methods=['POST'])
def remove():
    if 'user_id' not in session:
        return redirect('/login')
    targetid = request.form.get('target_id')
    equipment_id = request.form.get('equipment_id')
    remove_equipment(targetid, equipment_id)
    inventory = get_inventory_full_list()
    return jsonify(inventory=inventory)

# admin control add equipment
@app.route('/add_equipment', methods=['POST'])
def add_equipment_route():
    equipment = request.form.to_dict()
    add_equipment_to_pool(equipment)
    return jsonify({'success': True}), 200

def set_username_cookie(response, username):
    response.set_cookie('username', username)
    return response

def get_username_cookie(request):
    return request.cookies.get('username')

app.add_url_rule('/static/script.js', 'script', build_only=True)


if __name__ == '__main__':
    app.run(debug=True, port=3155)
