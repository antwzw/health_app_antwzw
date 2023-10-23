"""This is for check login page POST."""
import pathlib
import uuid
import hashlib
import os
import flask
from flask import redirect, url_for
import health


def login():
    """Login."""
    username = flask.request.form['username']
    password = flask.request.form['password']
    if not (username and password):
        flask.abort(400)
    # get the password saved in the database.
    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username == ?",
        (username, )
    )
    temp = cur.fetchall()
    if not temp:
        flask.abort(403)
    correct_password = temp[0]['password']
    salt = correct_password.split("$")[1]
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    # if the password not match, abort.
    if correct_password != password_db_string:
        flask.abort(403)
    # matches, create sessions.
    flask.session['username'] = username


def edit_account():
    """Edit_account."""
    if 'username' not in flask.session:
        flask.abort(403)
    fullname = flask.request.form['fullname']
    email = flask.request.form['email']
    logname = flask.session['username']
    connection = health.model.get_db()
    if not (fullname and email):
        flask.abort(400)
    if 'file' not in flask.request.files:
        connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ? "
            "WHERE username == ?", (fullname, email, logname, )
        )
    else:
        cur = connection.execute(
            "SELECT filename from users "
            "WHERE username == ?", (logname, )
        )
        result = cur.fetchall()
        filepath = health.app.config["UPLOAD_FOLDER"] \
            / result[0]["filename"]
        os.remove(filepath)
        fileobj = flask.request.files['file']
        filename = fileobj.filename
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"
        path = health.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)
        connection.execute(
            "UPDATE users "
            "SET filename = ?, fullname = ?, email = ? "
            "WHERE username == ?",
            (uuid_basename, fullname, email, logname, )
        )


def first_create():
    """Create."""

    username = flask.request.form['username']
    print(username)
    password = flask.request.form['password']
    if not (username and password):
        flask.abort(400)
    hash_obj = hashlib.new('sha512')
    salt = uuid.uuid4().hex
    hash_obj.update((salt + password).encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join(['sha512', salt, password_hash])

    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT username FROM users "
        "WHERE username == ?", (username, )
    )
    temp = cur.fetchall()
    if temp:
        flask.abort(409)
    cur = connection.execute(
        "INSERT INTO users "
        "(username,fullname,email,filename,password) "
        "VALUES (?,?,?,?,?); ", (username, "", "", "", password_db_string)
    )
    flask.session['username'] = username


def second_create():
    if 'username' not in flask.session:
        flask.abort(403)
    logname = flask.session['username']
    if 'file' not in flask.request.files:
        flask.abort(400)
    fileobj = flask.request.files['file']
    fullname = flask.request.form['fullname']
    email = flask.request.form['email']
    if not (fileobj and fullname and email):
        flask.abort(400)
    suffix = pathlib.Path(fileobj.filename).suffix.lower()
    uuid_basename = f"{uuid.uuid4().hex}{suffix}"
    path = health.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    connection = health.model.get_db()
    connection.execute(
        "UPDATE users "
        "SET filename = ?, fullname = ?, email = ? "
        "WHERE username == ?",
        (uuid_basename, fullname, email, logname, )
    )


def delete():
    """Delete."""
    if 'username' not in flask.session:
        flask.abort(403)
    logname = flask.session['username']
    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT filename from users "
        "WHERE username == ?", (logname, )
    )
    result = cur.fetchall()
    filepath = health.app.config["UPLOAD_FOLDER"] \
        / result[0]["filename"]
    os.remove(filepath)
    cur = connection.execute(
        "SELECT filename from posts "
        "WHERE owner == ?", (logname, )
    )
    results = cur.fetchall()
    for result in results:
        filepath = health.app.config["UPLOAD_FOLDER"] \
            / result["filename"]
        os.remove(filepath)
    cur = connection.execute(
        "DELETE FROM users "
        "WHERE username == ?", (logname, )
    )
    del flask.session['username']


def update():
    """Update."""
    if 'username' not in flask.session:
        flask.abort(403)
    password_entered = flask.request.form['password']
    new_password1 = flask.request.form['new_password1']
    new_password2 = flask.request.form['new_password2']
    if not (password_entered and new_password1 and new_password2):
        flask.abort(400)
    logname = flask.session['username']
    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT password from users "
        "WHERE username == ?", (logname, )
    )
    result = cur.fetchone()
    password = result["password"]
    salt = password.split("$")[1]
    hash_obj = hashlib.new('sha512')
    password_salted = salt + password_entered
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join(['sha512', salt, password_hash])
    if password != password_db_string:
        flask.abort(403)
    if new_password1 != new_password2:
        flask.abort(401)
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new('sha512')
    password_salted = salt + new_password1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join(['sha512', salt, password_hash])
    cur = connection.execute(
        "UPDATE users "
        "SET password = ? WHERE username == ?",
        (password_db_string, logname, )
    )


@health.app.route("/accounts/", methods=["POST"])
def check_login():
    """Transition pages. Check if the user \
        auenthentic successfully or not."""
    operation = flask.request.form['operation']
    target = flask.request.args.get('target')
    if not target:
        target = url_for('show_index')
    if operation == "login":
        if 'username' in flask.session:
            return redirect(url_for('show_index'))
        login()
    elif operation == "edit_account":
        edit_account()
    elif operation == "first_create":
        print("fuuuuuuuuu")
        first_create()
    elif operation == "second_create":
        second_create()
    elif operation == "delete":
        delete()
    elif operation == "update_password":
        update()
    return redirect(target)
