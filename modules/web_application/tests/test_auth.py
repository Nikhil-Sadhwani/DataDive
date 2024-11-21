from modules.web_application.models.models import User
from unittest.mock import patch

def mock_google_login():
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "picture": "http://example.com/picture.jpg"
    }

@patch('modules.web_application.views.auth.google.authorize_access_token')
@patch('modules.web_application.views.auth.google.get')
def test_google_login(mock_google_get, mock_authorize_access_token, client, init_database):
    mock_authorize_access_token.return_value = {"access_token": "test_token"}
    mock_google_get.return_value.json.return_value = mock_google_login()

    response = client.get('/authorize/google', follow_redirects=True)

    assert response.status_code == 200
    assert b"You have been logged in!" in response.data 
    
    user = User.query.filter_by(email="testuser@example.com").first()
    assert user is not None
    assert user.name == "Test User"
    assert user.email == "testuser@example.com"
