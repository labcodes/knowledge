import pytest
import re
from django.contrib.auth.models import User
from model_mommy import mommy
from links.models import Link
from requests.exceptions import ConnectionError
from tagging.models import Tag, TaggedItem


@pytest.mark.django_db
def test_index_view_redirect_response(client):
    response = client.get('/')

    assert response.status_code == 302


def log_user_in(client):
    user = User.objects.create(email='fernando@labcodes.com.br', username="fernando", is_staff=True)
    user.set_password("123456")
    user.save()

    return client.post('/auth/login/', {'username': user.email, 'password': '123456'}).data['auth_token']


@pytest.mark.django_db
def test_list_links_view_response(client):
    token = log_user_in(client)

    response = client.get('/links/',  HTTP_AUTHORIZATION='Token {}'.format(token))

    assert response.status_code == 200


@pytest.mark.django_db
def test_list_links_view_response_with_wrong_token(client):
    token = 'aadsiosdidsdsi'

    response = client.get('/links/',  HTTP_AUTHORIZATION='Token {}'.format(token))

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_new_link_api_view(client):

    token = log_user_in(client)

    response = client.post('/links/create/', {'title': 'Api Slack',
                                              'url': 'https://api.slack.com/',
                                              'tags': ''}, HTTP_AUTHORIZATION='Token {}'.format(token))

    assert response.status_code == 201


def test_create_link_view_unauthorized_to_use_get_method(client):
    response = client.get('/links/create/')

    assert response.status_code == 401


@pytest.mark.django_db
def test_slack_new_link_view_response(client, mock_slack_notification):
    response = client.post('/api/link/', {'text': 'https://teamtreehouse.com/home',
                                          'user_id': 'U3V3VMPFC'})

    link = Link.objects.all()[0]

    assert response.status_code == 201
    assert link.title == "Treehouse | Sign In"
    assert link.url == "https://teamtreehouse.com/home"


@pytest.mark.django_db
def test_slack_new_link_view_refuse_get_method(client, monkeypatch):
    response = client.get('/api/link/')

    assert response.status_code == 405


@pytest.mark.django_db
def test_slack_new_invalid_link_in_view(client):
    response = client.post('/api/link/', {'text': 'TreeHouse:https://teamtreehouse.com/home',
                                          'user_id': 'U3V3VMPFC'})

    assert response.data.get('text') == 'Your Link is not valid. Please check your url.'
    assert response.status_code == 400


@pytest.mark.django_db
def test_slack_new_invalid_link_in_link_manager(client, mock_slack_notification):
    with pytest.raises(ConnectionError):
        Link.objects.create_from_slack('http://raiseconnectionerror.com/', 'http://raiseconnectionerror.com/', 'U3V3VMPFC')
