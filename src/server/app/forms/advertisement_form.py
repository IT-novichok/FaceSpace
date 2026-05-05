from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, HiddenField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired


class AdvertisementForm(FlaskForm):
    cover_data = HiddenField(id='image-data')
    cover = FileField('Choose cover image', id='image-input')
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Write in detail about who you want to find.')
    category = SelectField('Choose category')
    submit = SubmitField('Publish')

    def __init__(self, categories, action='Publish'):
        super().__init__()
        self.category.choices = categories
        self.submit.label.text = action
