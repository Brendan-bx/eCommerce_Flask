from market import app
from flask import render_template, redirect, url_for, get_flashed_messages, flash
from market.model import Item, User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user

@app.route("/")

@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/market")
def market_page():
    return render_template('market.html', item_name=Item.query.all())

@app.route("/register", methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address = form.email.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There is an error while creating this user. The error is {err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Welcome {attempted_user.username}. You have successfully logged in", category="success")
            return redirect(url_for('market_page'))
        else:
            flash("Username and Password not matched. Please try again", category="danger")
    return render_template('login.html', form=form)