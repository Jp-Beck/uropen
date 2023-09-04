# main/routes.py
from flask import Blueprint
from flask import render_template, request, jsonify
from openur.models import Post

main = Blueprint('main', __name__)

# Routes
@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html', title='About')

@main.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@main.route('/documentation')
def documentation():
    return render_template('documentation.html', title='Documentation')

@main.route('/download')
def download():
    return render_template('download.html', title='Download')

@main.route('/database')
def database():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('database.html', title='Database', posts=posts)

# return posts in JSON format as an api
@main.route('/database/api')
def api():
    posts = Post.query.all()

    # Convert the list of Post objects to a list of dictionaries
    posts_list = [{
        'author': post.author.username,
        'title': post.title,
        'content': post.content,
        'date_posted': post.date_posted.strftime('%Y-%m-%dT%H:%M:%S')  # Convert datetime object to string
    } for post in posts]

    return jsonify(posts_list)