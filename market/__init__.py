from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_login import LoginManager 
from flask_cors import CORS
from flask_session import Session
from threading import Thread
import psycopg2
import secrets 
import os
import time






# kdmf
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://ad_e8lb_user:45fE7dwCPw9ZGFCUXRev3ewgWzun6Z61@dpg-cjra6q0jbais73bibk40-a.oregon-postgres.render.com:5432/ad_e8lb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://tatadb_user:JHUDOpY0em1PswBxEv7uYxKLZHilmQaB@dpg-cicfqfd9aq03rjn5173g-a.oregon-postgres.render.com:5432/tatadb (db connection)'


app.secret_key = 'f99fc1fcecf0e4da478694b54cea0dcd77c2b31b2d6a6230'
app.config['WTF_CSRF_ENABLED'] = False
#'postgresql://tatadb_user:JHUDOpY0em1PswBxEv7uYxKLZHilmQaB@dpg-cicfqfd9aq03rjn5173g-a.oregon-postgres.render.com:5432/tatadb'

db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.app_context().push()

# keep_alive.py


def keep_alive():
    with app.app_context():
        while True:
            try:
                db.session.execute("SELECT 1")  # A simple SQL query to keep the connection alive
                db.session.commit()
            except Exception as e:
                print(f"Error executing keep-alive query: {str(e)}")

            time.sleep(60)  # Sleep for 5 minutes (adjust as needed)

# Create a function to start the keep-alive thread
def start_keep_alive_thread():
    keep_alive_thread = Thread(target=keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start()



from market import routes
