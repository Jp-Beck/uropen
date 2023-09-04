# user/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from openur import db, bcrypt
from openur.models import User, Post
from openur.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetRequestForm, ResetPasswordForm
from openur.posts.forms import PostForm
from flask_login import login_user, current_user, logout_user, login_required
from openur.users.utils import _save_picture, send_reset_email


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    # If the user is already logged in, redirect to 'database'
    if current_user.is_authenticated:
        return redirect(url_for('main.database'))

    form = RegistrationForm()

    # If the form is not valid, render the register template
    if not form.validate_on_submit():
        return render_template('register.html', title='Register', form=form)

    # Hash the password and create a new user
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)

    # Add the user to the database and commit
    db.session.add(user)
    db.session.commit()

    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('users.login'))




@users.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to 'database'
    if current_user.is_authenticated:
        return redirect(url_for('main.database'))

    form = LoginForm()

    # If the form is not valid, render the login template
    if not form.validate_on_submit():
        return render_template('login.html', title='Login', form=form)

    user = User.query.filter_by(email=form.email.data).first()

    # Verify if user exists and the password is correct
    if user and bcrypt.check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        flash(f'Welcome back, {user.username}!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.database'))
    
    flash(f'Login unsuccessful. Please check Email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    flash(f'You have been logged out!', 'success')
    return redirect(url_for('main.index'))

@users.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()

    # Populate the form with the current user's information when accessed with a GET request
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    elif form.validate_on_submit():
        # Update user's image if they uploaded a new one
        if form.picture.data:
            current_user.image_file = _save_picture(form.picture.data)

        # Update user's other info
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('users.profile'))

    # Serve the profile page
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Profile', image_file=image_file, form=form)

@users.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # Get the post with the given id or return 404 if not found
    post = Post.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if post.author != current_user:
        flash(f'You are not authorized to update this post!', 'danger')
        return redirect(url_for('main.database'))

    form = PostForm()

    # If the form is not valid, render the update template
    if not form.validate_on_submit():
        form.title.data = post.title
        form.content.data = post.content
        return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

    # Update the post
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit()

    flash(f'Your post has been updated!', 'success')
    return redirect(url_for('posts.post', post_id=post.id))

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.database'))
    user = User.verify_reset_token(token) # static method in models.py
    if not user:
        flash(f'That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Hash the password and create a new user
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password

        # Add the user to the database and commit
        db.session.commit()

        flash(f'Your password has been updated! You can now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)