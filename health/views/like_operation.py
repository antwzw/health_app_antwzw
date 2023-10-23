"""This is for like POST."""
import flask
from flask import redirect, url_for
import health


@health.app.route("/likes/", methods=["POST"])
def like_operation():
    """Transition page. Manage the like and unlike operation."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    target = flask.request.args.get('target')
    operation = flask.request.form['operation']
    if not target:
        target = url_for('show_index')
    if operation == "unlike":
        postid = flask.request.form['postid']
        connection = health.model.get_db()
        cur = connection.execute(
            "SELECT * FROM likes "
            "WHERE owner == ? AND postid == ? ",
            (flask.session['username'], postid)
        )
        if not cur.fetchall():
            flask.abort(409)
        connection.execute(
            "DELETE FROM likes "
            "WHERE owner== ? AND postid == ? ",
            (flask.session['username'], postid)
        )
        return redirect(target)
    if operation == "like":
        postid = flask.request.form['postid']
        connection = health.model.get_db()
        cur = connection.execute(
            "SELECT * FROM likes "
            "WHERE owner == ? AND postid == ? ",
            (flask.session['username'], postid)
        )
        if cur.fetchall():
            flask.abort(409)
        connection.execute(
            "INSERT INTO likes(owner,postid) "
            "VALUES (?,?); ", (flask.session['username'], postid)
        )
        return redirect(target)
    return "default"
