


from app.blueprints.blog import blog
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import PostForm, RegisterAddressForm, SearchForm
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
    addressess = current_user.addressess.all()
    if form.validate_on_submit():
        name = form.name.data
        address = form.address.data
        phone = form.phone_number.data
        Address(name=name, address=address, phone_number=phone, user_id=current_user.id)
        return redirect(url_for('blog.index'))
    return render_template('register_address.html', title=title, form=form, addressess=addressess)

@blog.route('/my-addressess')
@login_required
def my_addressess():
    title = 'Your Addresses'
    addressess = current_user.addressess.all()
    return render_template('my_addressess.html', title=title, addressess=addressess)


@blog.route('/edit-address/<int:address_id>', methods=['GET', 'POST'])
@login_required
def edit_address(address_id):
    address = Address.query.get_or_404(address_id)
    if address.user_id != current_user.id:
        flash('You do not have access to this post', 'danger')
        return redirect(url_for('blog.my_addressess'))
    title = f"Edit {address.name}"
    form = RegisterAddressForm()
    if form.validate_on_submit():
        address.update(**form.data)
        flash(f'You have updated your address {address.name}', 'warning')
        return redirect(url_for('blog.my_addressess'))
    return render_template('address_edit.html', title=title, address=address, form=form)

## delete addresses
@blog.route('/delete-address/<int:address_id>')
@login_required
def delete_address(address_id):
    address = Address.query.get_or_404(address_id)
    if address.user_id != current_user.id:
        flash('You do not have access to delete this post', 'danger')
        return redirect(url_for('blog.my_addressess'))
    else:
        address.delete()
        flash(f'"{address.name}" has been deleted', 'secondary')
        return redirect(url_for('blog.my_addressess'))




############################
@blog.route('/search-posts', methods=['GET', 'POST'])
def search_posts():
    title = 'Search'
    form = SearchForm()
    posts = []
    if form.validate_on_submit():
        term = form.search.data
        posts = Post.query.filter((Post.title.ilike(f'%{term}%')) | (Post.body.ilike(f'%{term}%'))).all()
    return render_template('search_posts.html', title=title, posts=posts, form=form)


@blog.route('/posts/<post_id>')
@login_required
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = post.title
    return render_template('post_detail.html', title=title, post=post)


@blog.route('/edit-posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    if post_id != current_user.id:
        flash('You do not have access to this post', 'danger')
        return redirect(url_for('blog.my_posts'))
    post = Post.query.get_or_404(post_id)
    title = f"Edit {post.title}"
    form = PostForm()
    if form.validate_on_submit():
        post.update(**form.data)
        flash(f'You have updated your post {post.author}', 'warning')
    return render_template('post_edit.html', title=title, post=post, form=form)

@blog.route('/delete-posts/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have access to delete this post', 'danger')
        return redirect(url_for('blog.my_posts'))
    else:
        post.delete()
        flash(f'"{post.title}" has been deleted', 'secondary')
        return redirect(url_for('blog.my_posts'))