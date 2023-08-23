from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)


class Task:

    def __init__(self, task, due_date):
        self.task = task
        self.due_date = due_date
        self.complete = False


my_tasks = []


@app.route('/')
def index():
    return render_template("index.html", tasks=my_tasks)


@app.route('/add', methods=["POST"])
def add_task():
    task = request.form['task']
    date = request.form['date']
    new_task = Task(task, date)
    my_tasks.append(new_task)
    my_tasks.sort(key=lambda x: x.due_date)

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
