from flask_login import login_user
from modules.web_application.models.models import User

def test_prompt_generation(client, init_database):
    test_user = User.query.filter_by(email="testuser@example.com").first()
    login_user(test_user)

    response = client.post('/prompt', json={
        'prompt': 'What is the capital of France?'
    })

    assert response.status_code == 200
    assert b'Paris' in response.data
