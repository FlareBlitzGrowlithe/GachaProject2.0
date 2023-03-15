#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import make_response
from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from functools import wraps
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

# decorator for login check
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@login_required
def index():
    return render_template('login.html')

'''
@app.route('/register', methods=['GET'])
def show_register():
    return render_template('register.html')
'''

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    user_id = request.form.get('ids')
    print(request.form.to_dict())
    admin = False
    gold = 0
    luck = 50
    user = {"user_id":user_id, "username": username, "password": generate_password_hash(
        password), "admin": admin, "gold": gold, "luck": luck}
    print(user)
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
@login_required
def user():
    user = get_user_by_id(session['user_id'])
    print(session)
    print(user)
    inventory = get_equipment_by_userid(user["user_id"])
    if inventory==None:
        inventory={}
    return render_template('user.html', user=user, inventory=inventory)

# page /draw
@app.route('/draw')
@login_required
def draw():
    user = get_user_by_id(session['user_id'])
    inventory = get_equipment_by_userid(user["user_id"])
    username = get_username_cookie(request)
    return render_template('draw.html', user=user, inventory=inventory, username=username)

# TODO: page /store 
@app.route('/store')
@login_required
def store():
    user = get_user_by_id(session['user_id'])
    return render_template('store.html', user=user)

# page admin control
@app.route('/admin')
@login_required
def admin():
    user = get_user_by_id(session['user_id'])
    return render_template('admin.html', user=user)

# get full inventory list for admin page
@app.route('/getinventoryall')
@login_required
def get_inventory_all():
    inventory = get_inventory_full_list()
    return jsonify(inventory=inventory)

# get current user's inventory
@app.route('/getinventory')
@login_required
def get_inventory():
    user = get_user_by_id(session['user_id'])
    inventory = get_equipment_by_userid(user["user_id"])
    return jsonify(inventory=inventory)

# get full equipment list for form display
@app.route('/get_equipment_all')
@login_required
def get_equipment_all():
    equipment = get_equipment_full_list()
    return jsonify(equipment=equipment)

@app.route('/get_gold')
@login_required
def get_gold():
    user = get_user_by_id(session['user_id'])
    gold = user ["gold"]
    return jsonify(gold=gold)


@app.route('/update_gold', methods=['POST'])
@login_required
def set_gold():
    user_id = request.form.get('user_id')
    amount = request.form.get('amount')
    update_user_gold(user_id, amount)
    user = get_user_by_id(user_id)
    return jsonify(gold=amount, user=user)


@app.route('/update_luck', methods=['POST'])
@login_required
def set_luck():
    user_id = request.form.get('user_id')
    luck = request.form.get('luck')
    update_user_luck(user_id, luck)
    user = get_user_by_id(user_id)
    return jsonify(luck=luck, user=user)


@app.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect('/'))
    response.delete_cookie('username')
    return response

#gacha function
@app.route('/gacha', methods=['POST'])
@login_required
def gacha():
    user = get_user_by_id(session['user_id'])
    pool = request.form.get('pool')
    times = int(request.form.get('times'))
    [results, gold_left] = draw_gacha(pool, user, times)
    for result in results:
        if result!=[]:
            add_equipment_to_userid({"user_id": user["user_id"], "pool": pool,
                     "success_level": result['success_level'], 
                     "roll": result['roll'],
                     "equipment_id": result['ids']})
    return jsonify(results=results, gold=gold_left)

# sell item from user's inventory
@app.route('/sell', methods=['POST'])
@login_required
def sell():
    user = get_user_by_id(session['user_id'])
    equipment_id = request.form.get('equipment_id')
    sold = sell_equipment(user, equipment_id)
    if sold:
        inventory = get_equipment_by_userid(user["user_id"])
    return jsonify(inventory=inventory)

# remove item from user's inventory
@app.route('/remove', methods=['POST'])
@login_required
def remove():
    targetid = request.form.get('target_id')
    equipment_id = request.form.get('equipment_id')
    remove_equipment(targetid, equipment_id)
    inventory = get_inventory_full_list()
    return jsonify(inventory=inventory)

# admin control add equipment
@app.route('/add_equipment_admin', methods=['POST'])
@login_required
def add_equipment_admin():
    equipment = request.form.to_dict()
    add_equipment_to_pool(equipment)
    return jsonify({'success': True}), 200


# get all users from the database for display
@app.route('/get_users_all')
@login_required
def get_users():
    users = get_user_all()
    #user_list = [{'user_id': user.id, 'user_name': user.username}
    #         for user in users]
    return jsonify(users=users)

# add the selected equipment to the selected user's inventory in the database.
@app.route('/add_equipment_to_userid', methods=['POST'])
@login_required
def add_item_to_user():
    userid = request.form.get('user_id')
    equipment_id = request.form.get('equipment_id')
    add_equipment_to_userid(({"user_id": userid, "pool": "",
                              "success_level": "",
                              "roll": "",
                              "equipment_id": equipment_id}))
    return {}


def set_username_cookie(response, username):
    response.set_cookie('username', username)
    return response

def get_username_cookie(request):
    return request.cookies.get('username')

app.add_url_rule('/static/script.js', 'script', build_only=True)


@app.route('/hidden/shutdown/')
def shutdown_flask():
    func = request.environ.get('werkzeug.server.shutdown')
    if func != None:
        func()
    return jsonify({})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3211, debug=True, threaded=True)
