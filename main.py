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
    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/blog', methods= ['GET'])
def main_blog():
    blogs = Blog.query.all()
    return render_template('mainblog.html', blogs = blogs)

@app.route('/blog/<id>',methods= ['GET'])
def blogid(id):
    # id = request.args.get('id')
    indi_post = Blog.query.filter_by(id=id).first()
    print("individual=",indi_post.title,indi_post.body)
    return render_template('individualpost.html', indi_post= indi_post)

@app.route('/newpost', methods=['POST', 'GET'])
def new_blog():
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

            new_blog = Blog(blog_title,blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog')
   
    return render_template('newblog.html',title= 'Build a blog')
if __name__ == '__main__':
    app.run()
