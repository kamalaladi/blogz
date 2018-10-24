from flask import Flask, request, redirect, render_template,session,flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['DEBUG'] = True
# create connection string which connects to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:root@localhost:8889/blogz'

app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) # create db object. its an instance of sqlalchemy class
app.secret_key = os.urandom(24)
#create persistant class
#class that can be stored in the database

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self,title,body,owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref= 'owner')


    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    #list of routes that users dont have to log in to see
    allowed_routes = ['login','signup','index','mainblog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #TODO verify user's  password
        #allows us to select only the first result in a result set
        user = User.query.filter_by(username=username).first()
        #if checks does the user exist
        #if the user is not none from the query i.e if user exists then compare the password
        #then log in
        if user and user.password == password:
            #TODO "remember" that user has logged in

            session['username'] = username # next time the user log in the session object looks for that
            flash("Logged in")# flash messages use the session object to store the message for the next time the user comes back
            return redirect('/newpost')
        else:
            #TODO explain why login failed
            flash('User password incorrect, or user does not exist', 'error')
            #return '<h1>Error! <h1>

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data
        error = validate_user(username,password,verify)
        #find the user exists in the database with same username
        existing_user = User.query.filter_by(username=username).first()
            #if user does not exists create a new user
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] =username
            return redirect('/newpost')
        elif existing_user:
            # TODO - user better response messaging
            flash('user already exists',"error")
            
           

    return render_template('signup.html')

def validate_user(username,password,verify):
    error_msg = ""
    if username == "" or password == "" or verify == "":
        error_msg = "one or more fields are invalid"
        flash(error_msg,"error")
    elif password != verify:
        error_msg = "password does not match"
        flash(error_msg,"error")
    elif len(username)<3 or len(username)>20 or username == " ":
        error_msg = "Invalid username"
        flash(error_msg,"error")
    elif len(password)<3 or len(password)>20 or password == " ":
        error_msg = "Invalid password"
        flash(error_msg,"error")

    return error_msg

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


    
@app.route('/blog',methods= ['GET'])
def blogid():
    id = request.args.get('id')

    user = request.args.get('user')
    if id:
        indi_post = Blog.query.filter_by(id=id).first()
        print("individual=",indi_post.title,indi_post.body)
        return render_template('individualpost.html', indi_post= indi_post)

    if user:
        owner = User.query.filter_by(username=user).first()
        blogs = Blog.query.filter_by(owner = owner).all()

        return render_template("singleuser.html", blogs = blogs,owner=owner)
        
    else:
        blogs = Blog.query.all()
        user = User.query.all()
        return render_template('mainblog.html', blogs = blogs,user= user)
        

@app.route('/newpost', methods=['POST', 'GET'])
def new_blog():
    #get the owner of the blog
    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        blog_title =request.form['blogtitle']
        blog_body = request.form['blogbody']
        error_title = ""
        error_body = ""
        if blog_title == "" or blog_body == "":
            error_title = "Please fill in the title"
            error_body = "Please fill in the body "
            return render_template('newblog.html',title_error=error_title, body_error=error_body)
        else:

            new_blog = Blog(blog_title,blog_body,owner)

            db.session.add(new_blog)
            db.session.commit()
            user = owner.username
            return redirect('/blog?user='+ user)
   
    return render_template('newblog.html')


@app.route('/')
def index():
    users = User.query.all()

    return render_template('index.html',users = users)

        
if __name__ == '__main__':
    app.run()
