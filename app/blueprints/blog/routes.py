
from app.blueprints.auth.routes import login
from app.blueprints.blog import blog
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import PostForm, RegisterAddressForm
from .models import Post, Address

@blog.route('/') # app is the flask instance
def index():
    title = 'This is the homepage'
    posts = Post.query.all()
    return render_template('index.html', posts=posts, title=title)



@blog.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    title = 'Create A Post'
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        new_post = Post(title=title, body=body, user_id=current_user.id)
        flash(f"{new_post.title} has been created!", "secondary")
        return redirect(url_for('blog.index'))
    return render_template('create_post.html', title=title, form=form)

@blog.route('/my-posts')
@login_required
def my_posts():
    title = 'Your Posts'
    posts = current_user.posts.all()
    return render_template('my_posts.html', title=title, posts=posts)

@blog.route('/register-address', methods=['GET', 'POST'])
@login_required
def register_address():
    title = 'Register Address'
    form = RegisterAddressForm()
    addressess = current_user.addresses.all()
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        phone = form.phone_number.data
        Address(name=name, address=address, phone_number=phone, user_id=current_user.id)
        return redirect(url_for('blog.index'))
    return render_template('register_address.html', title=title, form=form, addressess=addressess)