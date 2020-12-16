from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
  
app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(20), default='N/A')
    date_posted = db.Column(db.DateTime , default=datetime.utcnow)

    def __repr__(self):
        return 'blog post' + str(self.id)

all_posts = [
    {
        'title' : 'post 1',
        'content' : 'about post 1',
        'author' : 'Ruthvik'
    },{
        'title' : 'post 2',
        'content' : 'about post 2'
    }
]
 
# @app.route('/<string:name>')  
# def home(name):  
#     return "hello, " + name ;  

@app.route('/')
def simple():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = blogpost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = blogpost.query.order_by(blogpost.date_posted).all()
        return render_template('posts.html', posting=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = blogpost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = blogpost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post = post)


if __name__ =='__main__':  
    app.run(debug = True)