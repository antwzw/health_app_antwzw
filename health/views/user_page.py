"""This is for user GET."""
import flask
from flask import redirect, url_for
import health


@health.app.route("/users/<user_url_slug>/")
def user_page(user_url_slug):
    """User page funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    context = {"logname": flask.session['username']}
    context["username"] = user_url_slug
    connection = health.model.get_db()
    # get fullname
    cur = connection.execute(
        "SELECT fullname, filename FROM users "
        "WHERE username == ? ",
        (user_url_slug,)
    )
    temp = cur.fetchall()
    if not temp:
        flask.abort(404)
    context["fullname"] = temp[0]["fullname"]
    context["img_url"] = "/uploads/"+temp[0]["filename"]
    # Count followings.
    cur = connection.execute(
        "SELECT COUNT(username1) FROM following "
        "WHERE username1 == ?",
        (user_url_slug,)
    )
    following = cur.fetchall()[0]
    following = list(following.values())[0]
    context["following"] = following
    # Count followers
    cur = connection.execute(
        "SELECT COUNT(username1) FROM following "
        "WHERE username2 == ?",
        (user_url_slug,)
    )
    followers = cur.fetchall()[0]
    followers = list(followers.values())[0]
    context["followers"] = followers
    cur = connection.execute(
        "SELECT * from posts "
        "WHERE owner == ?",
        (user_url_slug,)
    )
    posts = []
    context["total_posts"] = 0
    for post in cur.fetchall():
        context["total_posts"] += 1
        this_post = {}
        this_post["postid"] = str(post["postid"])
        this_post["img_url"] = "/uploads/"+post["filename"]
        posts.append(this_post)
    context["posts"] = posts
    # find relationship 1 for following,
    # 0 for not following, -1 for logname = username
    cur = connection.execute(
        "SELECT * from following "
        " Where username1 == ? AND username2 == ? ",
        (flask.session["username"], user_url_slug)
    )
    # following!
    if cur.fetchall():
        context["relationship"] = 1
    else:
        context["relationship"] = 0
    if user_url_slug == flask.session["username"]:
        context["relationship"] = -1

    # check if it is a user's own page.
    context["is_ownpage"] = 0
    if user_url_slug == flask.session["username"]:
        context["is_ownpage"] = 1

    return flask.render_template("user.html", **context)
