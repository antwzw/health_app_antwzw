"""This is for following GET."""
import flask
from flask import redirect, url_for
import health


@health.app.route("/users/<user_url_slug>/following/")
def user_following(user_url_slug):
    """Following funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    context = {
        "logname": flask.session['username'], "username": user_url_slug}
    followings = []
    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users "
        "WHERE username == ? ", (user_url_slug,)
    )
    temp = cur.fetchall()
    if not temp:
        flask.abort(404)
    cur = connection.execute(
        "SELECT username2 FROM following "
        "WHERE username1 == ?", (user_url_slug, )
    )
    for one in cur.fetchall():
        following = {}
        following["username"] = one["username2"]
        cur = connection.execute(
            "SELECT filename FROM users "
            "WHERE username = ?", (one['username2'], )
        )
        temp2 = cur.fetchall()
        if not temp2:
            flask.abort(404)
        following["user_img_url"] = "/uploads/" + \
            temp2[0]["filename"]
        cur2 = connection.execute(
            "SELECT username2 FROM following "
            "WHERE username1 == ?", (flask.session['username'], )
        )
        isfollow = False
        for username2 in cur2.fetchall():
            isfollow |= (one["username2"] == username2["username2"])
        following["logname_follows_username"] = isfollow
        followings.append(following)
    context["following"] = followings

    return flask.render_template("following.html", **context)
