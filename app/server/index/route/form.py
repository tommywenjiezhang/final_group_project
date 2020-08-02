from flask_wtf import FlaskForm as Form
from wtforms import PasswordField, StringField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
import re
from server.model.userModel import UserModel as User


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=6, max=255)])
    email = StringField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=255)])
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=6, max=255)]
    )
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    phoneNumber = StringField(
        'phone',
        validators=[DataRequired()]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    def validate_phoneNumber(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            phoneNumberValidator = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
            if  not phoneNumberValidator.match(field.data):
                raise ValidationError('Invalid phone number.')
        except:
            raise ValidationError('Invalid phone number.')

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        email = User.query.filter_by(email=self.email.data).first()
        username = User.query.filter_by(username=self.username.data).first()
        if email:
            self.email.errors.append("Email already registered")
            return False
        elif username:
            self.username.errors.append("User already registered Please login")
            return False
        return True


class ForgotForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(),  Length(min=6, max=255)])

    def validate(self):
        initial_validation = super(ForgotForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username).first()
        if not user:
            self.email.errors.append("This email is not registered")
            return False
        return True


class ChangePasswordForm(Form):
    password = StringField(
        'password',
        validators=[DataRequired(), Length(min=6, max=255)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )