"""health development configuration."""

import pathlib


# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'


# Secret key for encrypting cookies
SECRET_KEY = b'\xc2\x13~\xf4\xbe")\x94y\x99Ok\x9ec\x95Jbz\xff\x12\rh\'M'
SESSION_COOKIE_NAME = 'login'


# File Upload to var/uploads/
health_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = health_ROOT/'var'/'uploads'
CSS_FOLDER = health_ROOT/'var'/'css'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# Database file is var/health.sqlite3
DATABASE_FILENAME = health_ROOT/'var'/'health.sqlite3'
