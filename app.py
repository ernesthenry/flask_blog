from flask import Flask, jsonify, render_template,request, abort
import os
from flask_cors import CORS
from .models import app, setup_db, db_drop_and_create_all
from .models import Users, Posts

""" Endpoint to fetch all blogs or posts """
@app.route('/api/v1/posts', methods=['GET'])
def current_blogs():
    blogs = Posts.query.all()
    formatted_blogs = [blog.format_record() for blog in blogs]
    return jsonify({
            'success': True,
            'blogs': formatted_blogs,
            'number_of_blogs':len(formatted_blogs)
        }),200
    
""" Endpoint to fetch single post or  blog """
@app.route('/api/v1/posts/<int:post_id>',methods=['GET'])
def fetch_blog(post_id):
    post = Posts.query.filter(Posts.id == post_id).one_or_none()

    if post is None:
        return {'message': 'Post not found', 'error_code': '404'}, 404

    formatted_post = post.format_record()
    return jsonify({
        'success': True,
        'post': formatted_post
    }), 200


"""Endpoint to create a new blog or post"""
@app.route('/api/v1/new-post', methods=['POST'])
def add_blog():
    body = request.get_json()
    title = body.get('title', None)
    description = body.get('description', None)
    try:
         # Check if both 'title' and 'description' are provided in the request
        if not title or not description:
            return {'message': 'Title and description are required fields.', 'error_code': '422'}, 422

        new_blog = Posts(title=title, description=description)

        # Add the new blog to the database
        new_blog.insert()
        print("New Blog has been created successfully")

                
        return jsonify({
                'success': True,
                'created': new_blog.id,
                'Number of blogs': len(Posts.query.all())
            })
    except:
        abort(422)                      

def create_app(app,test_test_config=None):
    app.config['SECRET_KEY']='57324676734hjvbedhjewr9pp942312y89r321g8t7'
    with app.app_context():
        setup_db(app)
        CORS(app)
        db_drop_and_create_all() 
    return app
    
APP=create_app(app)

if __name__=="__main__":
    port= int(os.environ.get("PORT",5000))
    APP.run(host='127.0.0.1',port=port,debug=True)

    