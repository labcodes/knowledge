import pytest
from django.contrib.auth.models import User
from model_mommy import mommy


@pytest.mark.django_db
def test_valid_login_view(client):
    user = mommy.make(
        User,
        email='test@labcodes.com.br',
        username='test_user',
        is_staff=True)
    user.set_password("123456")
    user.save()

    response = client.post('/api/auth/login/', {'username': user.email, 'password': '123456'})

    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_login_view(client):
    response = client.post('/api/auth/login/', {'username': 'Error', 'password': 'Error'})

    assert 'Wrong email or password' in response.data['non_field_errors']
