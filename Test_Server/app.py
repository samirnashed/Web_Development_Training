import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM users WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your secret key' test


@app.route('/')
def index():
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=post)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        email = request.form['mail']
        passw = request.form['pass']

        if not first_name:
            flash('First Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (first_name, last_name,email,pass) VALUES (?, ?,?,?)',
                         (first_name, last_name,email,passw))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        first_name = request.form['first']
        last_name = request.form['last']
        email = request.form['mail']
        passw = request.form['pass']

        if not first_name:
            flash('First Name is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE users SET first_name = ?, last_name = ?, email = ?, pass = ?'
                         ' WHERE id = ?',
                         (first_name, last_name, email, passw,id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)
