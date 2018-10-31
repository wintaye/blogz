from flask import Flask, request, redirect, render_template, flash, session
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import jinja2
import os
from user_signup_formulas import user_is_valid

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:MyPassword@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'a;slkfjalskdfjl;aksdfj;alksdfjl;askdflksjfdlksjdfglk;'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    owner_id = db.relationship('Blog', backref='owner')
    
    def __init__(self, email, password, username):
        self.email = email
        self.password = password
        self.username = username

    def is_valid(self):
        if self.email and self.password and self.username:
            return True
        else:
            return False

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1500))
    created = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner_id, created=None):
        self.title = title
        self.body = body
        if created is None:
            created = datetime.utcnow()
        self.created = created
        self.owner_id = owner_id

    def is_valid(self):
        if self.title and self.body and self.created and self.owner_id:
            return True
        else:
            return False

# @app.before_request
# def require_login():
#     allowed_routes = ['login', 'signup', 'blog', 'index']
#     if request.endpoint not in allowed_routes and 'username' not in session:
#         return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged In!")
            return redirect('/blog')
        else:
            flash("Username not found or password incorrect :/")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/blog', methods=['GET', 'POST'])
def display_blog_post():
    # if request.method == 'POST':
    #     blogs = Blog.query.all()
    #     # user_id = request.args.get('user')
    #     # new_post = Blog.query.get(blogid)
    #     return render_template('single_post.html', title="New Blog Post", blogs=blogs)
    # else:  
        all_blog_posts = Blog.query.all()
        return render_template('all_blog_posts.html', title="All Blog Entries", all_blog_posts=all_blog_posts)

@app.route("/new_post", methods=['GET', 'POST'])
def new_entry():
    #add new blog post to db
    #if request is POST
    if request.method == 'POST':
        new_blog_title = request.form['title']
        new_blog_body = request.form['body']
        #owner_id = request.args.get('owner_id')
        #username = session['username']
        #new_blog_owner = User.query.filter_by(username=username).first()
        if not new_blog_title or not new_blog_body:
            flash("Please fill out all forms.")
            return render_template('new_post_form.html', title="Create a new blog post", new_blog_title=new_blog_title, new_blog_body=new_blog_body)
        else:
            new_blog_post = Blog(new_blog_title, new_blog_body, owner_id)
            db.session.add(new_blog_post)
            db.session.commit()
            url = "/blog?id=" + str(new_blog_post.id)
            return redirect(url)
    else:
        #if request is GET
        return render_template('new_post_form.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        password = request.form['password']
        verify_password = request.form['verify_password']
        username = request.form['username']
        email = request.form['email']
        password_error = ''
        email_error = ''
        blank_error = ''
        verify_password_error = ''
        email_error = ''
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username is taken.")
            return redirect('/signup')

        elif not user_is_valid(username, email, password, verify_password):
            return render_template('signup.html', email_error=email_error, verify_password_error=verify_password_error, email=email, username=username, blank_error=blank_error, password_error=password_error)
            
        else:
            session['username'] = username
            new_user = User(email, password, username)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/blog")

    else: 
        return render_template('signup.html')

@app.route("/singleUser")
@app.route("/singleUser/<user>")
def singleUser():
    user_name_fetch = request.args.get('user')
    user = User.query.filter_by(username=user_name_fetch).first()
    owner_id = request.args.get('owner_id')
    blogs = Blog.query.filter_by(owner_id=owner_id)
    return render_template('single_user.html', user=user, blogs=blogs)

@app.route("/single_post")
def singlepost():
    blogid = request.args.get('bid')
    if blogid:
        blog = Blog.query.get(blogid)
        return render_template('single_post.html', blog=blog)
    else: 
        all_blog_posts = Blog.query.all()
        return render_template('all_blog_posts.html', title="All Blog Entries", all_blog_posts=all_blog_posts)

@app.route("/")
def all_users():
    users = User.query.all()
    return render_template('all_users.html', title="All Users", users=users)

@app.route("/logout")
def logout():
    del session['username']
    return redirect('/blog')


if __name__=='__main__':
    app.run()

