"""from flask import ...: Import necessary modules from the Flask library to build a web application.
import os: Import the os module for interacting with the operating system.
from flask_cors import CORS: Import the CORS extension to enable Cross-Origin Resource Sharing for the API.
from .models import ...: Import the Flask app (app), database setup functions (setup_db and db_drop_and_create_all), and the database models (Users and Posts) from the models module in the current package."""
from flask import Flask, jsonify, render_template,request, abort
import os
from flask_cors import CORS
from .models import app, setup_db, db_drop_and_create_all
from .models import Users, Posts

""" Endpoint to fetch all blogs or posts """
@app.route('/api/v1/posts', methods=['GET'])
def current_blogs():
    # Query all posts from the database
    blogs = Posts.query.all()
    # Format the posts data into a list of dictionaries
    formatted_blogs = [blog.format_record() for blog in blogs]
    # Return the formatted posts in a JSON response
    return jsonify({
        'success': True,
        'blogs': formatted_blogs,
        'number_of_blogs': len(formatted_blogs)
    }), 200
    
""" Endpoint to fetch single post or blog """
@app.route('/api/v1/posts/<int:post_id>', methods=['GET'])
def fetch_blog(post_id):
    # Query a single post from the database based on the provided post_id
    post = Posts.query.filter(Posts.id == post_id).one_or_none()

    # Check if the post is not found
    if post is None:
        return {'message': 'Post not found', 'error_code': '404'}, 404

    # Format the post data into a dictionary
    formatted_post = post.format_record()
    # Return the formatted post in a JSON response
    return jsonify({
        'success': True,
        'post': formatted_post
    }), 200

""" Endpoint to delete single post or blog """
@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    # Query a single post from the database based on the provided post_id
    post = Posts.query.filter(Posts.id == post_id).one_or_none()

    # Check if the post is not found
    if post is None:
        return {'message': 'Post not found', 'error_code': '404'}, 404

    try:
        # Delete the post from the database
        post.delete()
        return {
            'message': 'Post deleted successfully',
              'success': True
              }, 200
    except Exception as e:
        # If an exception occurs (e.g., database error), return a 500 Internal Server Error status code
      

"""Endpoint to create a new blog or post"""
@app.route('/api/v1/new-post', methods=['POST'])
def add_blog():
    # Extract data from the request JSON
    body = request.get_json()
    title = body.get('title', None)
    description = body.get('description', None)

    try:
        # Check if both 'title' and 'description' are provided in the request
        if not title or not description:
            return {'message': 'Title and description are required fields.', 'error_code': '422'}, 422

        # Create a new post instance with the provided data
        new_blog = Posts(title=title, description=description)

        # Add the new post to the database
        new_blog.insert()

        # Return a success response with the post ID and the total number of posts
        return jsonify({
            'success': True,
            'created': new_blog.id,
            'Number of blogs': len(Posts.query.all())
        })
    except:
        # If an exception occurs (e.g., database error), return a 422 Unprocessable Entity status code
        abort(422)               

def create_app(app,test_test_config=None):
    app.config['SECRET_KEY']='57324676734hjvbedhjewr9pp942312y89r321g8t7'
    with app.app_context():
        setup_db(app)
        CORS(app)
        db_drop_and_create_all() 
    return app
    
APP=create_app(app)

if __name__ == "__main__":
    # Retrieve the port number from the environment variable or use 5000 as the default
    port = int(os.environ.get("PORT", 5000))
    # Run the Flask app with the specified host and port
    APP.run(host='127.0.0.1', port=port, debug=True)
    