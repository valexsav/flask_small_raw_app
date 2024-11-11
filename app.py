from flask import Flask, render_template, request, redirect, url_for

from db import (
    get_all_tasks,
    get_task_by_id,
    get_task_contents,
    add_task_to_db,
    delete_task_from_db,
    edit_task_in_db,
    get_tasks_sorted_by_param
)

app = Flask(__name__)


@app.route('/index')
def sort_tasks():
    sort_by = request.args.get('sort_by', default='priority')
    tasks = get_tasks_sorted_by_param(sort_by)
    return render_template('index.html', tasks=tasks)


@app.route('/')
def redirect_to_tasks():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template(
            'index.html',
            tasks=get_all_tasks()
        )


@app.route('/tasks/<int:task_id>/')
def task(task_id):
    task = get_task_by_id(task_id)
    content = get_task_contents(task_id)
    return render_template(
        'task.html',
        task=task,
        content=content
    )


@app.route('/index/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
            name = request.form.get('name')
            category = request.form.get('category')
            description = request.form.get('description')
            priority = request.form.get('priority')
            status = request.form.get('status')

            add_task_to_db(name, category, description, priority, status)
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('add_task.html')

@app.route('/index/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    delete_task_from_db(task_id)
    return redirect(url_for('index'))


@app.route('/index/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_task_by_id(task_id)
    if request.method == 'GET':
        return render_template('edit_task.html', task=task)
    elif request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        priority = int(request.form.get('priority'))
        status = request.form.get('status')
        edit_task_in_db(name, category, description, priority, status, task_id)
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
