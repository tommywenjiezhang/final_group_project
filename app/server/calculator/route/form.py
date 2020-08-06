from flask_wtf import FlaskForm as Form
from wtforms import PasswordField, StringField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
import re


class DatasetForm(Form):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description',validators=[DataRequired()])
    values = StringField('values',validators=[DataRequired()])

    def validate(self):
        initial_validation = super(DatasetForm, self).validate()
        if not initial_validation:
            return False
        return True
