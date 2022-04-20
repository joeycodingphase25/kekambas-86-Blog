from . import api
from .auth import basic_auth, token_auth
from flask import jsonify, request
from app.blueprints.blog.models import Post
from app.blueprints.auth.models import User

@api.route('/token')
@basic_auth.login_required
def index():
    user = basic_auth.current_user()
    token = user.get_token()

    return jsonify({'token' : token, 'expiration': user.token_expiration})

# Create a user
@api.route('/users/create', methods=["POST"])
def create_user():
    if not request.is_json:
        return jsonify({'error':'Your Request Content-Type Must Be Apllication/Json'}), 400
    data = request.json
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f'{field} must be in request body'}), 400
    username = data['username']
    email = data['email']
    password = data['password']
    new_user = User(username=username, email=email, password=password)
    return jsonify(new_user.to_dict()), 201

# Get all posts
@api.route('/posts')

def get_posts():
    posts = Post.query.all()
    print(posts)
    return jsonify([p.to_dict() for p in posts]) # needs to be a jsonifiable List, NOT a list of objects




# Gert a single post by id
@api.route('/posts/<int:post_id>')
def get_single_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

# create a post
@api.route('/posts/create', methods=['POST'])
@token_auth.login_required
def create_post():
    if not request.is_json:
        return jsonify({'error':'Your Request Content-Type Must Be Apllication/Json'}), 400
    data = request.json
    for field in ['title', 'body']:
        if field not in data:
            return jsonify({'error':f"{field} must be in request body"}), 400
    title = data['title']
    body = data['body']
    user_id = token_auth.current_user().id
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict())

# Edit a post from post man

@api.route("/edit-posts/<int:post_id>", methods=["PUT"]) #PUT IS FOR UPDATES
@token_auth.login_required
def edit_single_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = token_auth.current_user() # ensures user is user
    if post.author != current_user:  
        return jsonify({"Error" : "You do not have access to delete this post"}), 403
    data = request.json
    for key in data:
        if key not in {'title', 'body'}:
            return jsonify({"error": f"{key} not found in title or body"}), 400
    post.update(**data)
    return jsonify(post.to_dict())



# delete a post from postman

@api.route('/delete-posts/<int:post_id>', methods=['DELETE'])
@token_auth.login_required
def delete_single_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = token_auth.current_user()
    if post.author != current_user:  
        return jsonify({"Error" : "You do not have access to delete this post"}), 403
    post.delete()
    return jsonify({}), 204





