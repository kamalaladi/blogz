from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# create connection string which connects to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) # create db object. its an instance of sqlalchemy class
#create persistant class
#class that can be stored in the database

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    def __init__(title,body):
        self.tiltle = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_title =request.form['blogtitle']
        blog_body = request.form['blogbody']
        new_blog = Blog(blog_titile,blog_body)
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()
    return render_template('mainblog.html',title= 'Build a blog',blog=blogs)
if __name__ == '__main__':
    app.run()
