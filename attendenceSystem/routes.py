import os
import secrets
from PIL import Image
from flask import Flask, redirect, render_template, request,jsonify, url_for, session, flash
from attendenceSystem import app, db, bcrypt
from attendenceSystem.forms import RegistrationForm, LoginForm, UpdateAccountForm
from attendenceSystem.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/home")
def home():
    if current_user.is_authenticated:
        return render_template("studentPage.html", posts=posts)
    return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template('about.html', title='About')




@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        picture_file = save_picture(form.upload.data)
        user = User(rollno=form.rollno.data,name=form.name.data,image_file=picture_file, section=form.section.data ,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(rollno=form.id.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
        # if form.id.data == 2202310100107 and form.password.data == 'password':
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)

    output_size = (1000, 1000)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(rollno=form.rollno.data).first()
        # if bcrypt.check_password_hash(current_user.password, form.password.data):
        current_user.rollno = form.rollno.data
        current_user.name = form.name.data
        current_user.section = form.section.data
        current_user.email = form.email.data
        if form.upload.data:
            picture_file = save_picture(form.upload.data)
            current_user.image_file = picture_file
        # current_user.password = form.password.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
        # else:
        #     flash('Something went wrong' ,'danger')
    elif request.method == 'GET':
        form.rollno.data = current_user.rollno
        form.name.data = current_user.name
        form.section.data = current_user.section
        form.email.data = current_user.email
    image_file = url_for('static', filename='img/' + current_user.image_file)
    return render_template('account.html', title='Account',image_file=image_file, form=form)