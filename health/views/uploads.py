"""This is upload."""
import os
from flask import send_from_directory
import flask
import health


@health.app.route('/uploads/<name>')
def download_file(name):
    """Upload funtion."""
    path = os.path.join(health.app.config["UPLOAD_FOLDER"], name)
    if not os.path.isfile(path):
        flask.abort(404)
    return send_from_directory(health.app.config["UPLOAD_FOLDER"], name)


@health.app.route('/css/<name>')
def download_css(name):
    """Upload funtion."""
    path = os.path.join(health.app.config["CSS_FOLDER"], name)
    if not os.path.isfile(path):
        flask.abort(404)
    return send_from_directory(health.app.config["CSS_FOLDER"], name)
