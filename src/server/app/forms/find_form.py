from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired

class FindForm(FlaskForm):
    cover = FileField('Choose cover image')
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Write in detail about who you want to find.')
    category = SelectField('Choose category')
    tags = StringField('Write tags (#tag)')
    submit = SubmitField('Publish')
    def __init__(self, categories):
        super().__init__()
        self.category.choices=categories
