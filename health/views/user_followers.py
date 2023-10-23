"""This is for followwers GET."""
import flask
from flask import redirect, url_for
import health


@health.app.route("/users/<user_url_slug>/followers/")
def user_followers(user_url_slug):
    """Followers funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users WHERE username == ? ",
        (user_url_slug,)
    )
    if not cur.fetchall():
        flask.abort(404)
    followers = []
    context = {
        "logname": flask.session['username'], "username": user_url_slug}
    cur = connection.execute(
        "SELECT username1 FROM following "
        "WHERE username2 == ?",
        (user_url_slug, )
    )
    for one in cur.fetchall():
        follower = {}
        follower["username"] = one["username1"]
        cur = connection.execute(
            "SELECT filename FROM users "
            "WHERE username = ?",
            (one['username1'], )
        )
        temp1 = cur.fetchall()
        if not temp1:
            flask.abort(404)
        follower["user_img_url"] = "/uploads/" + \
            temp1[0]["filename"]
        cur1 = connection.execute(
            "SELECT username2 FROM following "
            "WHERE username1 == ?",
            (flask.session['username'], )
        )
        isfollow = False
        for username2 in cur1.fetchall():
            isfollow |= (one["username1"] == username2["username2"])
        follower["logname_follows_username"] = isfollow
        followers.append(follower)
    context["followers"] = followers

    return flask.render_template("followers.html", **context)
