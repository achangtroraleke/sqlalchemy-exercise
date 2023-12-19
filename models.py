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
    tags = db.relationship('Tag', secondary='posts_tags', backref='post')
    

    def edit_info(self, title=title, content= content):
        self.title = title
        self.content = content

class Tag(db.Model):
    
    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement=True)
    name = db.Column(db.String(10), nullable = False,)
    # posts = db.relationship('PostTag', backref='tag')

class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)