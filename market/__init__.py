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


# kdmf
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://ad_e8lb_user:45fE7dwCPw9ZGFCUXRev3ewgWzun6Z61@dpg-cjra6q0jbais73bibk40-a.oregon-postgres.render.com:5432/ad_e8lb'


# app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://tatadb_user:JHUDOpY0em1PswBxEv7uYxKLZHilmQaB@dpg-cicfqfd9aq03rjn5173g-a.oregon-postgres.render.com:5432/tatadb (db connection)'


app.secret_key = 'f99fc1fcecf0e4da478694b54cea0dcd77c2b31b2d6a6230'
app.config['WTF_CSRF_ENABLED'] = False
#'postgresql://tatadb_user:JHUDOpY0em1PswBxEv7uYxKLZHilmQaB@dpg-cicfqfd9aq03rjn5173g-a.oregon-postgres.render.com:5432/tatadb'

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.app_context().push()

from market import routes
