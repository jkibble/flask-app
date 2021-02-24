from stonks import app, db, Todo
from flask import render_template, request, redirect

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        task = Todo(content=content)

        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'Failed to delete'

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    task.content = request.form['content']

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'Error updating task'
