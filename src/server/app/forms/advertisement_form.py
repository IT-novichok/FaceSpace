from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, HiddenField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from ..services import category_service


class AdvertisementForm(FlaskForm):
    cover = HiddenField('Choose cover image',id='image-data')
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Write in detail about who you want to find.')
    category = SelectField('Choose category')
    submit = SubmitField('Publish')

    def __init__(self, action='Publish', advertisement=None):
        super().__init__()
        self.category.choices = [category.name.capitalize() for category in category_service.get_all_categories()]
        self.submit.label.text = action
        if advertisement:
            self.cover.data = advertisement.cover
            self.title.data = advertisement.title
            self.content.data = advertisement.content
            self.category.data = advertisement.category.name
