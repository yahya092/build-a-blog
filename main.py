from flask import Flask,render_template,request,redirect,session,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:yahya092@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))


    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route('/newpost',methods=['POST','GET'])
def newpost():

    if request.method == "POST":
        new_title = request.form["newpost_title"]
        new_post = request.form['newpost']
        new_entry = Blog(new_title,new_post)
        db.session.add(new_entry)
        db.session.commit()

        return redirect('/blog?id=' + str(new_entry.id))

    return render_template('newpost.html')  

@app.route('/blog',methods=['POST','GET'])
def blog():
    
    entry_id = request.args.get("id")
    if entry_id:
        post = Blog.query.filter_by(id=int(entry_id)).first()
        return render_template('entries.html',title=post.title, body=post.body)

    blogs = Blog.query.all()   
   
    return render_template('blog.html',blogs=blogs)   


@app.route("/")
def index():
    return redirect("/blog")

if __name__ == '__main__':
    app.run()