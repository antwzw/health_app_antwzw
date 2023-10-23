"""This is for post POST."""
import pathlib
import uuid
import os
import flask
from flask import redirect, url_for
import health


@health.app.route("/posts/", methods=["POST"])
def new_post():
    """Post funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    operation = flask.request.form['operation']
    target = flask.request.args.get('target')
    if not target:
        target = f"/users/{flask.session['username']}/"
    if operation == "create":
        if 'file' not in flask.request.files:
            flask.abort(400)
        fileobj = flask.request.files['file']
        suffix = pathlib.Path(fileobj.filename).suffix.lower()
        uuid_basename = f"{uuid.uuid4().hex}{suffix}"
        fileobj.save(health.app.config["UPLOAD_FOLDER"]/uuid_basename)
        connection = health.model.get_db()
        connection.execute(
            "INSERT INTO posts(filename, owner) "
            "VALUES (?, ?)", (uuid_basename, flask.session['username'])
        )
        return redirect(target)
    if operation == "delete":
        connection = health.model.get_db()
        postid = flask.request.form['postid']
        cur = connection.execute(
            "SELECT * FROM posts "
            "WHERE owner == ? AND postid == ? ",
            (flask.session['username'], postid)
        )
        temp = cur.fetchall()
        if not temp:
            flask.abort(403)
        cur = connection.execute(
            "DELETE FROM posts WHERE postid == ?", (postid, )
        )
        filepath = health.app.config["UPLOAD_FOLDER"] \
            / temp[0]["filename"]
        os.remove(filepath)
        return redirect(target)
    return "default"
