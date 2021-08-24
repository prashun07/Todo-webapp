from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__) # here we created instance of class Flask. '__name__' is a package which tells flask where to look resources like in static or template.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

#GET and  POST is HTTP methods,by default methods have GET methods but other methods can also be added.
#GET	It is the most common method which can be used to send data in the unencrypted form to the server.
#POST	It is used to send the form data to the server. The server does not cache the data transmitted using the post method.
#PUT	It is used to replace all the current representation of the target resource with the uploaded content.
@app.route('/', methods=['GET', 'POST']) #route() in a decorator which tells what url will trigger function written below. 
def input():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

#in <int:sno> sno is a variable where as int is type of convertible. there are 5 types of convertible in flask,int,string,float,path and uuid.
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    delete_sn = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delete_sn)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
