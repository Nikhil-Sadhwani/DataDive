from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()



class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    social_login_provider = db.Column(db.String(50), nullable=True)

    profile_picture = db.Column(db.String(200), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))



    scraped_data = db.relationship('ScrapedData', backref='user', lazy=True)

    prompt_logs = db.relationship('PromptLog', backref='user', lazy=True)



    @property 

    def is_active(self):

        return True

    

    @property 

    def is_authenticated(self): 

        return True 

    

    @property 

    def is_anonymous(self): 

        return False



    def get_id(self): 

        return str(self.id)



class ScrapedData(db.Model):
    """
    Model to store scraped web data
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2048), nullable=False)
    content = db.Column(db.Text, nullable=True)
    data_metadata = db.Column(db.JSON, nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<ScrapedData {self.url}>'



class PromptLog(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    prompt_text = db.Column(db.Text, nullable=False)

    generated_output = db.Column(db.Text, nullable=False)

    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc)) 

    tokens_used = db.Column(db.Integer, nullable=False)
