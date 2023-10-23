"""
health index (main) view.

URLs include:
/
"""
import flask
from flask import redirect, url_for
import arrow
import health
import datetime


@health.app.route('/')
def show_index():
    """Show the index page."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    logname = flask.session['username']
    connection = health.model.get_db()
    show_posts = [logname]
    # the index page should include all posts from the
    # logged in user and all other users that the
    # logged in user is following.
    # So we filter those users out first.
    cur = connection.execute(
        "SELECT username2 from following "
        "WHERE username1 == ?", (logname, )
    )
    show_posts += [di["username2"] for di in cur.fetchall()]
    show_posts = str(tuple(show_posts))
    if show_posts[-2] == ",":
        temp = list(show_posts)
        temp[-2] = " "
        show_posts = "".join(temp)
    context = {"logname": logname}
    cur = connection.execute(
        "SELECT * from posts "
    )
    posts = []
    for post in cur.fetchall():
        this_post = {}
        cur = connection.execute(
            "SELECT filename from users "
            "WHERE username == ?", (post["owner"], )
        )
        this_post["owner_img_url"] = "/uploads/" + cur.fetchone()["filename"]
        this_post["postid"] = str(post["postid"])
        this_post["owner"] = post["owner"]
        this_post["img_url"] = "/uploads/"+post["filename"]
        this_post["timestamp"] = arrow.get(post["created"]).humanize()
        this_post["created_time"] = arrow.get(post["created"])
        cur = connection.execute(
            "SELECT fullname FROM users "
            "WHERE username == ? ",
            (this_post["owner"],)
        )
        temp = cur.fetchone()
        if not temp:
            flask.abort(404)
        this_post["fullname"] = temp["fullname"]
        cur = connection.execute(
            "SELECT owner from likes "
            "WHERE postid == ?", (this_post["postid"],)
        )
        likes = cur.fetchall()
        this_post["likes"] = len(likes)
        # find out if the login user like this post.
        likes = [di["owner"] for di in likes]
        if logname in likes:
            this_post["like_this_post"] = 1
        else:
            this_post["like_this_post"] = 0
        # deal with comments.
        cur = connection.execute(
            "SELECT owner,text,created FROM comments "
            "WHERE postid == ?", (this_post["postid"],)
        )
        comments = cur.fetchall()
        comments.sort(key=lambda x: x["created"])
        this_post["comments"] = comments

        posts.append(this_post)
    posts.sort(key=lambda x: x["postid"], reverse=True)
    context["posts"] = posts
    print(posts)
    context["date"] = datetime.date.today()
    return flask.render_template("index.html", **context)
