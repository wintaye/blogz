from flask import Flask, request, redirect, render_template, flash
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
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.relationship('Blog', backref='owner_id'))
    
    def __init__(self, id, email, password):
        self.id = user_id
        self.email = email
        self.password = password

    def is_valid(self):
        if self.id and self.email and self.password:
            return True

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1500))
    created = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, created=None):
        self.title = title
        self.body = body
        if created is None:
            created = datetime.utcnow()
        self.created = created
        self.owner_id = owner_id

    def is_valid(self):
        if self.title and self.body and self.created:
            return True
        else:
            return False

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route("/", methods=['GET', 'POST'])
def index():
    return redirect("/login")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/blog')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html')
    
@app.route("/validate", methods=['POST'])
def validate():
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']
    template = jinja_env.get_template('signup_form.html')
    return render_template(username=username, password=password, verify_password=verify_password, email=email)

@app.route("/blog", methods=['GET', 'POST'])
def display_blog_posts():
    #display all posts or new blog post page
    blog_id = request.args.get('id')
    if blog_id:
        blog = Blog.query.get(blog_id)
        #blog = Blog.query.order_by(blog_id.desc()).all()
        return render_template('single_post.html', title="New Blog Post", blog=blog)
    else:  
        all_blog_posts = Blog.query.all()
        return render_template('all_blog_posts.html', title="All Blog Entries", all_blog_posts=all_blog_posts)

#@app.route('/new_post')
#def make_new_post():
    #return render_template('new_post_form.html')

@app.route("/new_post", methods=['POST'])
def new_entry():
    #add new blog post to db
    if request.method == 'POST':
        new_blog_title = request.form['title']
        new_blog_body = request.form['body']
        new_blog_post = Blog(new_blog_title, new_blog_body)
        if new_blog_post.is_valid():
            db.session.add(new_blog_post)
            db.session.commit()
            url = "/blog?id=" + str(new_blog_post.id)
            return redirect(url)
        else:
            flash("Please check your entry for errors. Both a post title + body are required.")
            return render_template('new_post_form.html', title="Create a new blog post", new_blog_title=new_blog_title, new_blog_body=new_blog_body)

@app.route("/signup", methods=['POST', 'GET'])
def validation():
    if request.method == 'POST':
        password = request.form['password']
        verify_password = request.form['verify_password']
        username = request.form['user']
        email = request.form['email']
        if user_is_valid(username, email, password, verify_password):
            db.session.add(email, password)
            db.session.commit()
            return redirect('/blog')
        else: 
            return render_template('signup.html', email_error=email_error, verify_password_error=verify_password_error, email=email, username=username, blank_error=blank_error, password_error=password_error)

@app.route('/singleuser')
def singleUser():
    all_single_user = request.args.get('user')
    user = User.query.filter_by(user=user_name_fetch).first()
    return render_template('single_user.html', title=user, all_single_user=all_single_user)


if __name__=='__main__':
    app.run()

