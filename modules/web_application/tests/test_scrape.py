from flask_login import login_user
from modules.web_application.models.models import User

def test_web_scraping(client, init_database):
    test_user = User.query.filter_by(email="testuser@example.com").first()
    login_user(test_user)

    response = client.post('/scrape', data={
        'url': 'https://example.com'
    })

    assert response.status_code == 200
    assert b'Scraping successful' in response.data  
