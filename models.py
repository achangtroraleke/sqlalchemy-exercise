"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)
    
   
    

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key =True,
                   autoincrement=True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    image_url = db.Column(db.Text, nullable=True)

    def edit_info(self, first_name=first_name, last_name= last_name, image_url=image_url):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement=True)
    
    title = db.Column(db.String(100), nullable = False)
    content =  db.Column(db.String(50), nullable = False)
    created_at = db.Column(db.DateTime, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref = 'posts')

    def edit_info(self, title=title, content= content):
        self.title = title
        self.content = content