from market import app
from flask import (
    render_template,
    redirect,
    url_for,
    get_flashed_messages,
    flash,
    request,
)
from market.model import Item, User
from market.forms import RegisterForm, LoginForm, purchaseform, sellform
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchase_form = purchaseform()
    sell_form = sellform()
    if request.method == "POST":
        purchased_item = request.form.get("purchase_item")
        P_item_obj = Item.query.filter_by(name=purchased_item).first()
        if P_item_obj:
            if current_user.can_buy(P_item_obj):
                P_item_obj.buy()
                flash(
                    f"You have succesfully bought {P_item_obj.name} for {P_item_obj.price}",
                    category="success",
                )
                return redirect(url_for("market_page"))
            else:
                flash(f"Sorry You have insufficient fund to buy")
        sell_item = request.form.get("sell_item")
        s_item_obj = Item.query.filter_by(name=sell_item).first()
        if s_item_obj:
            if current_user.can_sell(current_user):
                s_item_obj.sell(current_user)

        return redirect(url_for("market_page"))

    if request.method == "GET":
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template(
            "market.html",
            item_name=Item.query.filter_by(owner=""),
            purchase_form=purchase_form,
            owned_items=owned_items,
            sell_form=sell_form,
        )

    return render_template(
        "market.html",
        item_name=Item.query.filter_by(owner=""),
        purchase_form=purchase_form,
    )


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email.data,
            password=form.password1.data,
        )
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f"There is an error while creating this user. The error is {err_msg}",
                category="danger",
            )
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f"Welcome {attempted_user.username}. You have successfully logged in",
                category="success",
            )
            return redirect(url_for("market_page"))
        else:
            flash(
                "Username and Password not matched. Please try again", category="danger"
            )
    return render_template("login.html", form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    flash("Vous avez été déconnecté avec succées", category="info")
    return redirect(url_for("home_page"))
