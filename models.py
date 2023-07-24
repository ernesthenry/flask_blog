import os # This imports the os module, which provides a way to interact with the operating system. It is commonly used for tasks like handling file paths, environment variables, and other system-related operations.
"""These imports are from the Flask framework, a popular web application framework for Python. Here's a brief explanation of each:
Flask: This is the main class of the Flask framework and is used to create an instance of the web application.
render_template: This function is used to render HTML templates in Flask. It allows you to generate dynamic HTML pages using template files.
request: This is a global object provided by Flask that represents the current HTTP request being processed. It allows you to access data sent with the request (e.g., form data, query parameters).
url_for: This function is used to build URLs for specific routes or functions in your Flask application. It abstracts the URL generation and allows you to refer to routes by their function names.
redirect: This function is used to perform HTTP redirects to a specified URL. It is commonly used after processing a form submission to redirect the user to a different page.
"""
from flask import Flask, render_template, request, url_for, redirect

"""This imports the SQLAlchemy class from flask_sqlalchemy module. SQLAlchemy is an Object-Relational Mapping (ORM) library that provides a high-level interface for working with databases in Flask applications. It simplifies database operations and allows you to interact with the database using Python classes and objects."""
from flask_sqlalchemy import SQLAlchemy
"""This imports the Migrate class from flask_migrate module. Flask-Migrate is an extension for Flask that helps with database migrations. It provides a way to handle changes in your database schema and keep it in sync with your application's models."""
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

# Setup the database for the Flask app.
def setup_db(app):
    # Database configuration.
    database_name = 'sql'
    default_database_path = "postgresql://{}:{}@{}/{}".format('postgres', 123, 'localhost:5432', database_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = default_database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set up the database with the app.
    db.app = app
    db.init_app(app)

# Drop and create all tables in the database.
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

# Define the Users model for the 'users' table.
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(100))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    def insert(self):
        # Add the user instance to the database session and commit changes.
        db.session.add(self)
        db.session.commit()

# Define the Posts model for the 'blogs' table.
class Posts(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def insert(self):
        # Add the post instance to the database session and commit changes.
        db.session.add(self)
        db.session.commit()

    def update(self):
        # Commit changes to update the post in the database.
        db.session.commit()

    def delete(self):
        # Delete the post from the database.
        db.session.delete(self)
        db.session.commit()

    def format_record(self):
        # Format the post data to a dictionary.
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }
"""The comments added to the code should help you understand the purpose of each function, model, and configuration. This code sets up a Flask app with a SQLAlchemy database and defines two models (Users and Posts) that correspond to two different database tables (users and blogs). The models include methods for inserting, updating, deleting records, and formatting data. """






