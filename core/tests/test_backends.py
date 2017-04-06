import pytest
from django.contrib.auth.models import User
from model_mommy import mommy


@pytest.mark.django_db
def test_valid_login_view(client):
    user = User.objects.create(email='fernando@labcodes.com.br', username="fernando", is_staff=True)
    user.set_password("123456")
    user.save()

    response = client.post('/auth/login/', {'username': user.email, 'password': '123456'})

    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_login_view(client):
    response = client.post('/auth/login/', {'username': 'Error',
                                             'password': 'Error'})

    assert 'Wrong email or password' in response.data['non_field_errors']
