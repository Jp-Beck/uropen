# post/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from openur import db
from openur.models import Post
from openur.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!', 'success')
        return redirect(url_for('main.database'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
    # Get the post with the given id or return 404 if not found
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)



@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    # Get the post with the given id or return 404 if not found
    post = Post.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if post.author != current_user:
        flash(f'You are not authorized to delete this post!', 'danger')
        return redirect(url_for('main.database'))

    # Delete the post
    db.session.delete(post)
    db.session.commit()

    flash(f'Your post has been deleted!', 'success')
    return redirect(url_for('main.database'))
