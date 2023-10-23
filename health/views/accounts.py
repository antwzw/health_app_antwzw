"""This is for account page GET."""
import flask
from flask import redirect, url_for
import health


@health.app.route('/firstpage/')
def show_firstpage():
    """Show the first page."""
    return flask.render_template("firstpage.html")


@health.app.route('/add/')
def show_add():
    """Show the add page."""
    return flask.render_template("adddata.html")


@health.app.route('/chat/<user>/')
def show_chatuserpage(user):
    """Show the chat page."""
    logname = flask.session["username"]
    context = {"username": user, "logname": logname}
    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT * FROM comments "
        "WHERE username == ? and owner == ?", (user, logname)
    )
    comments = cur.fetchall()
    cur = connection.execute(
        "SELECT owner,text,created, username FROM comments "
        "WHERE username == ? and owner == ?", (logname, user)
    )
    comments.extend(cur.fetchall())
    print(comments)
    comments.sort(key=lambda x: x["created"])
    context["comments"] = comments
    return flask.render_template("chatuser.html", **context)


@health.app.route('/chat/')
def show_chatpage():
    """Show the chat page."""
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
    return flask.render_template("chat.html", **context)


@health.app.route('/accounts/login/')
def acc_login():
    """Show Account login pages."""
    if 'username' not in flask.session:
        return flask.render_template("login.html")
    return redirect(url_for("show_index"))


@health.app.route("/accounts/logout/", methods=["post"])
def acc_logout():
    """Accout logout funtion."""
    operation = flask.request.form['operation']
    if operation == "first_create":
        if 'username' not in flask.session:
            return redirect("/firstpage/")
        del flask.session['username']
        return redirect("/firstpage/")
    elif operation == "second_create":
        if 'username' not in flask.session:
            return redirect("/firstpage/")
        del flask.session['username']
        return redirect("/accounts/first_create/")


@health.app.route('/accounts/first_create/')
def acc_first_create():
    """Show Account create pages."""

    if 'username' not in flask.session:
        return flask.render_template("first_create.html")

    return redirect(url_for("acc_edit"))


@health.app.route('/accounts/second_create/')
def acc_second_create():
    """Show Account create pages."""

    return flask.render_template("second_create.html")


@health.app.route('/accounts/delete/')
def acc_delete():
    """Show Account delete pages."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    logname = flask.session['username']
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>health</title>
    </head>
    <div>
        <h2 style="float: left;"><a href="/">logo</a> | health</h2>
        <h2 style="float: right;"><a href="/explore/">explore</a> | \
        <a href="/users/{logname}/">{logname}</a></h2>
    </div>
    <div style="clear: both;">
        {logname}
        <form action="/accounts/?target=/accounts/create/" \
            method="post" enctype="multipart/form-data">
            <input type="submit" name="delete" value="confirm delete account"/>
            <input type="hidden" name="operation" value="delete"/>
        </form>
    </div>
    '''


@health.app.route("/accounts/edit/")
def acc_edit():
    """Account edit funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    logname = flask.session['username']
    connection = health.model.get_db()
    cur = connection.execute(
        "SELECT username, fullname, email, filename from users "
        "WHERE username == ?", (logname, )
    )
    context = cur.fetchone()
    return flask.render_template("edit.html", **context)


@health.app.route("/accounts/password/")
def acc_pwd():
    """Acc_pwd funtion."""
    if 'username' not in flask.session:
        return redirect("/firstpage/")
    logname = flask.session['username']
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>health</title>
    </head>
    <div>
        <h2 style="float: left;"><a href="/">logo</a> | health</h2>
        <h2 style="float: right;"><a href="/explore/">explore</a> | \
        <a href="/users/{logname}/">{logname}</a></h2>
    </div>
    <div style="clear: both;">
        <form action="/accounts/?target=/accounts/edit/" \
            method="post" enctype="multipart/form-data">
            Old password <input type="password" \
                name="password" required/>
            <br> New password <input type="password" \
                name="new_password1" required/>
            <br> New password, again <input type="password" \
                name="new_password2" required/>
            <br> <input type="submit" name="update_password" \
                value="submit"/>
            <input type="hidden" name="operation" value="update_password"/>
        </form>
        <br><a href="/accounts/edit/">Back to edit account</a>
    </div>
    '''
