from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, IntegerField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField
import email_validator


##WTForm
class ContactMeMessage(FlaskForm):
    subject = StringField(label="Subject", validators=[DataRequired()])
    name = StringField("First Name and Last Name:", validators=[DataRequired()])
    phone_number = IntegerField("Phone Number:", validators=[DataRequired()])
    e_mail = EmailField("Email Address:", validators=[DataRequired(), Email()])
    message = CKEditorField("Message:", validators=[DataRequired()])
    submit = SubmitField("Send")

