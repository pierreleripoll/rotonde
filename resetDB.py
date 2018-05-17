from flask import *
from werkzeug.utils import secure_filename
import os
import re
from model import *
from model import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseRotonde.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False


db = SQLAlchemy(app)

with app.app_context() :
    db.reflect()
    db.drop_all()
    db.create_all()
