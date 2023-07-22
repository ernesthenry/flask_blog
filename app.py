import os
from flask import Flask
from flask_cors import CORS
from models import app, setup_db, db_drop_and_create_all

def create_app(app,test_test_config=None):
    app.config['SECRET_KEY']='57324676734hjvbedhjewr9pp942312y89r321g8t7'
    with app.app_context():
        setup_db(app)
        CORS(app)
        db_drop_and_create_all() 
    return app
    
app=create_app(app)

if __name__=="__main__":
    port= int(os.environ.get("PORT",5000))
    aPP.run(host='127.0.0.1',port=port,debug=True)

    