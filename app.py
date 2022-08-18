from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    #repr method prints todo's object
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    #We dont need to print the todo in terminal
    #print(allTodo) 
    return render_template("index.html", allTodo = allTodo)


@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return "This is you"

@app.route('/update/<int:sno>', methods = ['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno = sno).first()
    return render_template("update.html", todo = todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__== "__main__":
    app.run(debug=True, port=8000)
    #In testing we have to do the debug as True but in the production server we can't do 
    # we have use debug as False in production server so this will not show the exact error for the user.