"""This is for post GET."""
import flask
from flask import redirect, url_for
import arrow
import health


@health.app.route('/posts/<postid_url_slug>/')
def post(postid_url_slug):
    """Post funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    context = {"logname": flask.session['username']}
    context["postid"] = postid_url_slug
    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT * FROM posts "
        "WHERE postid == ?",
        (postid_url_slug, )
    )
    this_post = cur.fetchone()
    context["owner"] = this_post["owner"]
    cur = connection.execute(
        "SELECT filename FROM users "
        "WHERE username == ?",
        (this_post['owner'], )
    )
    context["owner_img_url"] = "/uploads/" + cur.fetchone()["filename"]
    context["img_url"] = "/uploads/" + this_post["filename"]
    context["timestamp"] = arrow.get(this_post["created"]).humanize()
    cur = connection.execute(
        "SELECT COUNT(likeid) FROM likes "
        "WHERE postid == ?",
        (postid_url_slug, )
    )
    context["likes"] = list(cur.fetchone().values())[0]
    cur = connection.execute(
        "SELECT COUNT(likeid) FROM likes "
        "WHERE postid == ? and owner == ?",
        (postid_url_slug, flask.session['username'])
    )
    context["like_this_post"] = list(cur.fetchone().values())[0]
    cur = connection.execute(
        "SELECT commentid, owner, text FROM comments "
        "WHERE postid == ?",
        (postid_url_slug)
    )
    context["comments"] = cur.fetchall()

    return flask.render_template("post.html", **context)
