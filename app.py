from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    filter_status = request.args.get('filter', 'all')

    conn = get_db_connection()

    if filter_status == 'pending':
        tasks = conn.execute('SELECT * FROM tasks WHERE status="Pending"').fetchall()
    elif filter_status == 'done':
        tasks = conn.execute('SELECT * FROM tasks WHERE status="Done"').fetchall()
    else:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()

    conn.close()
    return render_template('index.html', tasks=tasks, filter_status=filter_status)

@app.route('/add', methods=('POST',))
def add():
    task = request.form['task']
    priority = request.form['priority']
    due_date = request.form['due_date']

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO tasks (task, status, priority, due_date) VALUES (?, ?, ?, ?)',
        (task, 'Pending', priority, due_date)
    )
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/toggle/<int:id>')
def toggle(id):
    conn = get_db_connection()
    task = conn.execute('SELECT status FROM tasks WHERE id=?', (id,)).fetchone()

    new_status = "Done" if task["status"] == "Pending" else "Pending"

    conn.execute('UPDATE tasks SET status=? WHERE id=?', (new_status, id))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)