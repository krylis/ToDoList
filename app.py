from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"

db = SQLAlchemy()
db.init_app(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String, nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    complete = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    my_tasks = Tasks.query.order_by(Tasks.due_date)
    return render_template("index.html", tasks=my_tasks)


@app.route('/add', methods=["POST"])
def add_task():
    task = request.form['task']
    date_str = request.form['date']
    if date_str == '':
        date = datetime.utcnow()
    else:
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
    db.session.add(Tasks(task=task, due_date=date))
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Tasks.query.get_or_404(task_id)
    task.complete = True
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
