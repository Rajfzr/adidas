from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import LoginManager 
from flask_cors import CORS
from flask_session import Session
import psycopg2
import secrets 
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://tatadb_user:JHUDOpY0em1PswBxEv7uYxKLZHilmQaB@dpg-cicfqfd9aq03rjn5173g-a.oregon-postgres.render.com:5432/tatadb'
app.secret_key = '34cf4c8bc7f9e40bdcc0d1281e282346ea276ecd54b01c8cc08732e445cd'
app.config['WTF_CSRF_ENABLED'] = False
#'postgresql://tatadb_user:JHUDOpY0em1PswBxEv7uYxKLZHilmQaB@dpg-cicfqfd9aq03rjn5173g-a.oregon-postgres.render.com:5432/tatadb'

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.app_context().push()

from market import routes
