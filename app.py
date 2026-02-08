from flask import Flask, render_template , request , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db= SQLAlchemy(app)



class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=True)
    date_created=db.Column(db.DateTime,default= datetime.utcnow)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"


@app.route("/", methods = ['GET','POST'])
def hello_world():
    if request.method=="POST":
        title = request.form['title']
        description = request.form['description']
        todo = Todo(title = title, description = description)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for("hello_world"))
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@app.route("/clear", endpoint="clear_all")
def clear_all():
   db.session.query(Todo).delete()
   db.session.commit()
   return redirect(url_for("hello_world"))
 


@app.route("/products")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    
    return "<p>these are the products!</p>"

@app.route("/update/<int:sno>", methods = ['GET','POST'])
def update(sno):
    if request.method=='POST':
          title = request.form['title']
          description = request.form['description']
          todo = Todo.query.filter_by(sno=sno).first()
          todo.title=title
          todo.description=description
          db.session.add(todo)
          db.session.commit()
          return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)
    
    
    return "<p>these are the products!</p>"


@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    
    return redirect("/")

if __name__ =="__main__":
     app.run(debug=True, port=8000)