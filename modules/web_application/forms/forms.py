from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL

class ScrapeURLForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Scrape')

class PromptForm(FlaskForm):
    prompt_text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Generate')