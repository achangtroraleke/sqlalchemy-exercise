"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import connect_db, db, User
from sqlalchemy import text

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

# if __name__ == '__main__':
#     app.run(debug=True)