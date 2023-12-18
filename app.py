"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import connect_db, db, User, Post
from sqlalchemy import text
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)


@app.route('/', methods=["GET", "POST"])
def index():
    all_users = User.query.all()
    context = {'users':all_users}
    return render_template('home.html', context=context)

@app.route('/create-user/', methods=["GET",'POST'])
def add_user():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        img = request.form['img']
        print(first_name)
        new_user = User(first_name=first_name, last_name=last_name, image_url=img)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('create_user.html')
    
@app.route('/user/<int:user_id>/')
def show_user(user_id):
    print(user_id)
    user = User.query.get_or_404(user_id)

    
    return render_template('user-page.html', user= user)

@app.route('/delete/user/<int:user_id>/')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/edit/user/<int:user_id>/', methods=['GET','POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        img = request.form['img']

        user.edit_info(first_name, last_name, img)
        print(user)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    edit = True
    return render_template('create_user.html', edit = edit, user=user)

@app.route('/user/<int:user_id>/posts/new/', methods=['GET', 'POST'])
def post_page(user_id):
    curr_user = User.query.get(user_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(
            title = title,
            content = content,
            created_at = datetime.datetime.now(),
            author_id = user_id,
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/user/{user_id}/')

    return render_template('post_form.html', user = curr_user)

@app.route('/posts/<int:post_id>/', methods=['GET'])
def post_detail(post_id):
    curr_post = Post.query.get(post_id)
    return render_template('post_page.html', curr_post = curr_post)


@app.route('/posts/<int:post_id>/edit/', methods=['GET',"POST"])
def edit_post(post_id):
    curr_post = Post.query.get(post_id)
    if request.method =="POST":
        print('print', curr_post)
        title = request.form['title']
        content = request.form['content']
        curr_post.edit_info(title, content)
        print(curr_post)
        db.session.add(curr_post)
        db.session.commit()
        return redirect(f'/posts/{curr_post.id}/')

    
    return render_template('post_form.html', edit = True, curr_post=curr_post)

@app.route('/posts/<int:post_id>/delete/')
def delete_post(post_id):
    curr_post = Post.query.get(post_id)
    db.session.delete(curr_post)
    db.session.commit()
    return redirect('/')

# if __name__ == '__main__':
#     app.run(debug=True)