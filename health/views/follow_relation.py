"""This is for follow POST."""
import flask
from flask import redirect, url_for
import health


@health.app.route('/following/', methods=["post"])
def follow_relation():
    """Following funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    operation = flask.request.form["operation"]
    target = flask.request.args.get('target')
    if not target:
        target = url_for("show_index")
    connection = health.model.get_db()
    logname = flask.session["username"]
    if operation == "follow":
        cur = connection.execute(
            "SELECT * FROM following "
            "WHERE username1 == ? AND username2 == ? ",
            (logname, flask.request.form["username"])
        )
        if cur.fetchall():
            flask.abort(409)
        connection.execute(
            "INSERT INTO following(username1,username2)"
            "VALUES ( ? , ? );",
            (logname, flask.request.form["username"])
        )
    elif operation == "unfollow":
        cur = connection.execute(
            "SELECT * FROM following "
            "WHERE username1 == ? AND username2 == ? ",
            (logname, flask.request.form["username"])
        )
        if not cur.fetchall():
            flask.abort(409)
        connection.execute(
            "DELETE FROM following "
            "WHERE username1 ==? AND username2 ==? ",
            (logname, flask.request.form["username"])
        )
    return redirect(target)
