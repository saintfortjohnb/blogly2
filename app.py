"""Blogly application."""
from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

def create_and_configure_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "2023blogly"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    debug = DebugToolbarExtension(app)

    connect_db(app)

    with app.app_context():
        db.create_all()

    return app

app = create_and_configure_app()

@app.route('/')
def home():
    """Redirect to list of users"""
    return redirect("/users")

@app.route('/users')
def users_index():
    """Show list of users"""
    users = User.query.all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url'] or None  # use None if the field is empty
        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')

    else:
        return render_template('users/new.html')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show detail about user"""
    user = User.query.get_or_404(user_id)
    return render_template('users/detail.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Show edit form and handle edit"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url'] or None
        db.session.commit()

        return redirect(f'/users/{user_id}')

    else:
        return render_template('users/edit.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def create_post(user_id):
    """Create a new post"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content, user=user)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/users/{user_id}')

    else:
        return render_template('posts/new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/<int:post_id>')
def post_detail(user_id, post_id):
    """Show detail about a post"""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post_detail.html', user=user, post=post)

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(user_id, post_id):
    """Show edit form and handle edit for a post"""
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()

        return redirect(f'/users/{user_id}/posts/{post_id}')

    else:
        return render_template('posts/edit_post.html', user=user, post=post)

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

if __name__ == "__main__":
    app.run(debug=True)
