import pytest
from django.contrib.auth.models import User
from model_mommy import mommy


@pytest.mark.django_db
def test_valid_login_view(client):
    user = mommy.make(User)
    response = client.post('/accounts/login/', {'username': user.email,
                                             'password': user.password})

    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_login_view(client):
    response = client.post('/accounts/login/', {'username': 'Error',
                                             'password': 'Error'})

    assert 'Wrong email or password' in response.context['form'].errors.get('__all__')
