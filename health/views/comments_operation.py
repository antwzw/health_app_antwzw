"""This is for comments POST."""
import flask
from flask import redirect, url_for
import health


@health.app.route("/comments/", methods=["POST"])
def comments_operation():
    """Transition page. Deal with comments POST."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    target = flask.request.args.get('target')
    operation1 = flask.request.form['operation']
    if not target:
        target = url_for("show_index")
    if operation1 == "create":
        owner = flask.session['username']
        username = flask.request.form['username']
        text = flask.request.form['text']
        if not text:
            flask.abort(400)
        connection = health.model.get_db()
        connection.execute(
            "INSERT INTO comments(owner,username,text, postid) "
            "VALUES (?,?,?,?);", (owner, username, text, 0)
        )
        return redirect(target)
    if operation1 == "delete":
        connection = health.model.get_db()
        commentid = flask.request.form["commentid"]
        cur = connection.execute(
            "SELECT owner FROM comments "
            "WHERE commentid == ?",
            (commentid, )
        )
        if cur.fetchone()["owner"] != flask.session["username"]:
            flask.abort(403)
        connection.execute(
            "DELETE FROM comments WHERE commentid == ?", (commentid, )
        )
        return redirect(target)
    return "default"
