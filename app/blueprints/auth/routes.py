
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import SignUpForm, LoginForm
from .models import User


@auth.route('/sign-up', methods=["GET", "POST"])
def signup():
    title = 'Sign Up'
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
    #check if user exists
        users_with_that_info = User.query.filter((User.username==username)|(User.email==email)).all()
        if users_with_that_info:
            flash(f"There is a User with that user and/or email already", "warning")
            return redirect(url_for('blog.index'))

        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has successfully signed up.", "success")
        return redirect(url_for('blog.index'))

    return render_template('signup.html', title=title, form=form)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Log In'
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Check if there is a user with that username
        user = User.query.filter_by(username=username).first()
        #check if user and password true
        if user and user.check_password(password):
            # log in the user
            login_user(user)
            flash(f"{user} has successfully logged in", "success")
            # redirect
            return redirect(url_for('blog.index'))
        else:
            flash('Username and/or Password inccorrect, try again!', 'danger')
    return render_template('login.html', title=title, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have successfully logged out', 'primary')
    return redirect(url_for('blog.index'))


