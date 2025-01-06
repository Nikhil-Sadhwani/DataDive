from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, URL, Optional, Length

class ScrapeURLForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Scrape')

class PromptForm(FlaskForm):
    prompt_text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Generate')

class ScrapedDataForm(FlaskForm):
    """
    Form for editing scraped data
    """
    url = StringField('URL', 
        validators=[
            DataRequired(message="URL is required"),
            URL(message="Invalid URL format")
        ],
        render_kw={
            "placeholder": "Enter the scraped URL",
            "class": "form-control"
        }
    )
    
    content = TextAreaField('Content', 
        validators=[
            Optional(),
            Length(max=10000, message="Content is too long (max 10000 characters)")
        ],
        render_kw={
            "placeholder": "Scraped content",
            "class": "form-control",
            "rows": 5
        }
    )
    
    metadata = TextAreaField('Metadata', 
        validators=[
            Optional(),
            Length(max=1000, message="Metadata is too long (max 1000 characters)")
        ],
        render_kw={
            "placeholder": "Additional metadata (will be converted to JSON)",
            "class": "form-control",
            "rows": 3
        }
    )
    
    submit = SubmitField('Update Scraped Data', 
        render_kw={
            "class": "btn btn-primary"
        }
    )