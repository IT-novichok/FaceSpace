from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, DateField, SelectField
from wtforms.fields.simple import HiddenField, TelField
from wtforms.validators import DataRequired, email


class SettingsForm(FlaskForm):
    name = StringField('Name')
    nickname = StringField('Nickname')
    email = EmailField('Email')
    password = PasswordField('New password')
    password_again = PasswordField('Repeat password')
    birth_date = DateField('Brith date')
    gender = SelectField('Gender', choices=('Male', 'Female'))
    avatar = HiddenField('Select avatar', id='image-data')
    about = TextAreaField('About')
    phone_number = TelField('Phone Number')
    website = StringField('Website')
    socials = StringField('Socials')
    submit = SubmitField('Save')

    def __init__(self, user=None):
        super().__init__()
        if user:
            self.name.data = user.name
            self.nickname.data = user.nickname
            self.email.data = user.email
            self.birth_date.data = user.birth_date
            self.gender.data = user.gender
            self.avatar.data = user.avatar
            self.about.data = user.about
            self.phone_number.data = user.contacts.get('phone number')
            self.website.data = user.contacts.get('website')
            self.socials.data = user.contacts.get('socials')
