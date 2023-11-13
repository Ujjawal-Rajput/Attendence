from datetime import datetime
from attendenceSystem import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    # add p and a column also.
    # __tablename__ = 'User'  # Specify the actual table name in your database
    id = db.Column(db.Integer, primary_key=True, unique=True) #unique number id
    rollno = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    section = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # is_coordinator = db.Column(db.Boolean, default=False)
    # totalPresents = db.Column(db.Integer, nullable=False, default=0)
    # totalAbsents = db.Column(db.Integer, nullable=False, default=0)


    def __repr__(self):
        return f"User('{self.id}', '{self.rollno}', '{self.name}','{self.image_file}', '{self.section}', '{self.email}', '{self.password}')"


class Post(db.Model):
    # __tablename__ = 'Post'  # Specify the actual table name in your database
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


#need location table and section table(6 sections)
#function to add a section (new table) and set his coordinator (no need to set this),ask students to register themselves.

#add functionaliy to change or set class coordinates (because classes can be merged , changed)

#dlib @ file:///C:/Users/rujja/OneDrive/Desktop/attendence/dlib-19.24.1-cp311-cp311-win_amd64.whl#sha256=6f1a5ee167975d7952b28e0ce4495f1d9a77644761cf5720fb66d7c6188ae496