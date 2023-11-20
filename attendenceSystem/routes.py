import os
import secrets
from PIL import Image
from flask import Flask, redirect, render_template, request,jsonify, url_for, session, flash
from attendenceSystem import app, db, bcrypt
from attendenceSystem.forms import RegistrationForm, LoginForm, UpdateAccountForm
from attendenceSystem.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime
import geopy.distance


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


# def auth():
#     if current_user.is_authenticated and current_user.section != 'Coordinator':
#         return True
#     return False

@app.route("/studentPage")
def studentPage():
    if current_user.is_authenticated and current_user.section != 'Coordinator':
        return render_template("studentPage.html", posts=posts)
    return redirect(url_for('login'))

@app.route("/coordinatorPage")
def coordinatorPage():
    if current_user.is_authenticated and current_user.section == 'Coordinator':
        return render_template("coordinatorPage.html", posts=posts)
    return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template('about.html', title='About')




@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # print(current_user.section)
        if current_user.section == 'Coordinator':
            return redirect(url_for('coordinatorPage'))
        else:
            return redirect(url_for('studentPage'))
    
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
    # print(current_user)
    # if current_user.is_authenticated and current_user.section != 'Coordinator':
    #     # print(current_user.section)
    #     return redirect(url_for('studentPage'))
    # elif current_user.is_authenticated and current_user.section == 'Coordinator':
    #     return redirect(url_for('coordinatorPage'))


    if current_user.is_authenticated:
        # print(current_user.section)
        if current_user.section == 'Coordinator':
            return redirect(url_for('coordinatorPage'))
        else:
            return redirect(url_for('studentPage'))

    form = LoginForm()
    if form.validate_on_submit():
        useris = User.query.filter_by(rollno=form.id.data).first()
        # if (form.id.data==123 and form.password.data==000):
        #     login_user(user, remember=form.remember.data)
        #     return redirect(url_for('coordinatorPage'))
        # if form.id.data == 2202310100107 and form.password.data == 'password':
        if useris and bcrypt.check_password_hash(useris.password, form.password.data):
            login_user(useris, remember=form.remember.data)
            if (useris.rollno==123):
                return redirect(url_for('coordinatorPage'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('studentPage'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('studentPage'))


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
            # print(current_user.image_file)
            # path = os.path.join(app.config["IMAGE_UPLOADS"], current_user.image_file)  
            # os.remove(path)
            # path = os.path.join( image.filename)
            # if os.path.exists(url_for('static', filename='img/' + current_user.image_file)):
            # os.remove(url_for('static', filename='img/' + current_user.image_file))
            # print(current_user.image_file)
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


def is_student_in_classroom(student_coordinates,class_coordinates):
    threshold_distance=0.07 #in km
    distance = geopy.distance.distance(class_coordinates,student_coordinates)
    print(distance)
    return distance <= threshold_distance

@app.route('/process_frame', methods=['POST'])
def process_frame():
    student_latitude = request.form.get("latitude")
    student_longitude = request.form.get("longitude")
    print(student_latitude)
    print(student_longitude)
    # students_latitude=28.682085
    # student_longitude=77.341755
    student_coordinates=(student_latitude,student_longitude)
    # class_coordinates=(28.73632768718917, 77.48282227507165) #rd
    class_coordinates=(28.681776187231414, 77.34231361360732) #bansal kirana store
    #28.682080771681647, 77.34172937700261

    if is_student_in_classroom(student_coordinates,class_coordinates):
        pass
    else:
        return jsonify({"message": "Not in college"})
    
    image_path=os.path.join(app.root_path, 'static/img', current_user.image_file)
    user_image = face_recognition.load_image_file(image_path) #session user image-profile
    user_encoding = face_recognition.face_encodings(user_image)[0]

    known_face_encoding = [user_encoding]
    known_faces_names = [current_user.name] #session user name-username
    students = known_faces_names.copy()
    try:
        # Receive and process video frames from JavaScript
        frame_data = request.files['frame']  # Get the frame data from the client

        if frame_data is None:
            return jsonify({"error": "No frame data received"})

        # Read the frame data and decode it
        frame_bytes = frame_data.read()
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Check if the frame is empty or not successfully decoded
        if frame is None:
            return jsonify({"error": "Invalid frame format"})

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding, face_encoding)
            name = ''
            face_distance = face_recognition.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            # if name in students:
            #     # students.remove(name)
            #     print(students)
            #     current_time = now.strftime("%H-%M-%S")
            #     lnwriter.writerow([name, current_time])
        print(face_names)
        if face_names==['']:
            return jsonify({"message": "Face isn't matching"})
        elif face_names==[]:
            return jsonify({"message": "face is out of focus"})
        
        return jsonify({"recognized_faces": face_names})
        # return render_template('studentPage.html')
        # flash('Present marked', 'success')
    except Exception as e:
        return jsonify({"error": str(e)})