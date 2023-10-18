from flask import Flask, redirect, render_template, request,jsonify, url_for, session, flash,make_response
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from datetime import datetime

# from flask_session import Session
# from flask_mail import Mail,Message
app=Flask(__name__)
app.config["UPLOAD_FOLDER"]="static/img"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

