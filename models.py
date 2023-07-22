import os
from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
db= SQLAlchemy()
migrate=Migrate(app,db)

def setup_db(app):

    database_name='blog'
    default_database_path="postgresql://{}:{}@{}/{}".format('blog',123,'localhost:5432',database_name)
    app.config['SQLALCHEMY_DATABASE_URI']=default_database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.app=app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

class Users(db.Model):
    __tablename__='users'

    id=db.Column(db.Integer(), primary_key=True)
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    username=db.Column(db.String(100))

    def __init__ (self,email,username,password):
        self.email=email
        self.username=username
        self.password=password

    def insert(self):
        db.session.add(self)
        db.session.commit()


class Posts(db.Model):
    __tablename__='blogs'

    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String(100),unique=True)
    description=db.Column(db.String(100))
    

    def __init__ (self,name,description):
        self.name=name
        self.description=description

    def insert(self):
        db.session.add(self)
        db.session.commit()