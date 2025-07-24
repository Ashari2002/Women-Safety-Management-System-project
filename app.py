from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import math
import requests
import json

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
app.permanent_session_lifetime = timedelta(days=7)

# MySQL Configuration
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'women_safety_portal')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Initialize MySQL in utils
from app.models.utils import init_mysql
init_mysql(mysql)

# Import routes after app initialization to avoid circular imports
from app.routes.auth_routes import auth_blueprint
from app.routes.women_routes import women_blueprint
from app.routes.admin_routes import admin_blueprint
from app.routes.police_routes import police_blueprint

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(women_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(police_blueprint)

# Main route
@app.route('/')
def index():
    return render_template('index.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)