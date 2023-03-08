from flask import Flask
from .utils.database import *
from .utils.user import *
from .utils.equipment import *
from .utils.inventory import *
from .utils.gacha import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
