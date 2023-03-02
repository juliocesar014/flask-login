from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from accounts.models import User


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address"), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    
    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email address already in use")
            return False
        
        return True
    
    
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email(message="Please enter a valid email address"), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired()])