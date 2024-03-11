from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    

@app.route("/", methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('desc')
        if title and desc:  # Ensure title and desc are not empty
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template("home.html", allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        # db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update_page.html', todo=todo)

@app.route("/delete/<int:serialNo>")
def delete(serialNo):
    print(serialNo)
    delete_todo = Todo.query.filter_by(sno=serialNo).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect("/")

@app.route("/update_page")
def update_page():
    return render_template ('update_page.html')



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

