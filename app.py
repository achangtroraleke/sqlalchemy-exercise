"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import connect_db, db, User, Post, Tag
from sqlalchemy import text
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

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
    all_tags = Tag.query.all()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        active_tags = request.form.getlist('tags')
        
        new_post = Post(
            title = title,
            content = content,
            created_at = datetime.datetime.now(),
            author_id = user_id,
        )
        [new_post.tags.append(Tag.query.get(tag_id)) for tag_id in active_tags]
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/user/{user_id}/')

    return render_template('post_form.html', user = curr_user, tags = all_tags)

@app.route('/posts/<int:post_id>/', methods=['GET'])
def post_detail(post_id):
    curr_post = Post.query.get(post_id)
    return render_template('post_page.html', curr_post = curr_post)


@app.route('/posts/<int:post_id>/edit/', methods=['GET',"POST"])
def edit_post(post_id):
    all_tags = Tag.query.all()
    curr_post = Post.query.get(post_id)
    if request.method =="POST":
        title = request.form['title']
        content = request.form['content']
        curr_post.edit_info(title, content)
        active_tags = request.form.getlist('tags')
        curr_post.tags = [Tag.query.get(tag_id) for tag_id in active_tags]
       
        db.session.add(curr_post)
        db.session.commit()
        return redirect(f'/posts/{curr_post.id}/')

    
    return render_template('post_form.html', edit = True, curr_post=curr_post, tags = all_tags)

@app.route('/posts/<int:post_id>/delete/')
def delete_post(post_id):
    curr_post = Post.query.get(post_id)
    db.session.delete(curr_post)
    db.session.commit()
    return redirect(f'/user/{curr_post.author_id}')

@app.route('/tags/')
def all_tags():
    all_tags = Tag.query.all()
    return render_template('tag.html', tags = all_tags)

@app.route('/tags/<int:tag_id>/')
def get_tag(tag_id):
    curr_tag = Tag.query.get(tag_id)
    return render_template('tag_detail.html', tag = curr_tag)

@app.route('/tags/new/', methods=['GET','POST'])
def create_tag():
    
    if request.method == "POST":
        new_tag_name= request.form['tag']
        print(new_tag_name)
        new_tag = Tag(name = new_tag_name)
        db.session.add(new_tag)
        db.session.commit()
        return redirect('/tags/')
    return render_template('tag_form.html')

@app.route('/tags/<int:tag_id>/edit/', methods=['GET', 'POST'])
def edit_tag(tag_id):
    curr_tag = Tag.query.get(tag_id)
    if request.method == "POST":
        curr_tag.name = request.form['tag']
        db.session.add(curr_tag)
        db.session.commit()
        return redirect(f'/tags/{curr_tag.id}')
    return render_template('tag_form.html', tag = curr_tag, edit=True)

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    curr_tag = Tag.query.get(tag_id)
    db.session.delete(curr_tag)
    db.session.commit()
    return redirect(f'/tags/')

if __name__ == '__main__':
    app.run(debug=True)