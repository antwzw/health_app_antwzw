"""This is for explore GET."""
import flask
from flask import redirect, url_for
import health


@health.app.route('/explore/')
def explore():
    """Explore funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    context = {"logname": flask.session["username"]}
    connection = health.model.get_db()
    cur2 = connection.execute(
        "SELECT * FROM users "
        "WHERE username != ?",
        (flask.session['username'], )
    )
    users = []
    for one in cur2.fetchall():
        user_img_url = "/uploads/" + one["filename"]
        users.append(
            {"username": one["username"], "user_img_url": user_img_url, "fullname": one["fullname"]})
    context["users"] = users
    return flask.render_template("explore.html", **context)
