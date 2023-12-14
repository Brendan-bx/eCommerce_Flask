from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from market.model import User

class RegisterForm(FlaskForm):

  def validate_username(self, username_to_check):
    user = User.query.filter_by(username=username_to_check.data).first()
    if user:
      raise ValidationError("Username already exists. Please try a different username.")
  
  def validate_email(self, email_to_check):
    email = User.query.filter_by(email_address=email_to_check.data).first()
    if email:
      raise ValidationError("Email address already registered in the site.")

  username = StringField(label="Username: ", validators=[Length(min=5,max=30), DataRequired()])
  email = StringField(label="Email Address: ", validators=[Email(), DataRequired()])
  password1 = PasswordField(label= "Password: ", validators=[Length(min=5), DataRequired()])
  password2 = PasswordField(label="Confirm Password: ", validators=[EqualTo('password1'), DataRequired()])
  submit = SubmitField(label= "Register")

class LoginForm(FlaskForm):
    username = StringField(label="Username: ", validators=[DataRequired()])
    password = PasswordField(label= "Password: ", validators=[DataRequired()])
    submit = SubmitField(label="Login")


class PurchaseForm(FlaskForm):
  submit = SubmitField(label="Purchase!")


class SellForm(FlaskForm):
  submit = SubmitField(label="Sell")
