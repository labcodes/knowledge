import pytest
import re
from django.contrib.auth.models import User
from model_mommy import mommy
from unittest.mock import patch
from links.models import Link
from core.services.slack import get_slack_user, create_author
from core.services.utils import send_created_user_email


@pytest.mark.django_db
def test_index_view_redirect_response(client):
    response = client.get('/')

    assert response.status_code == 302


@pytest.mark.django_db
def test_list_links_view_response(client):
    response = client.get('/links/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_list_links_template_name(client):
    response = client.get('/links/')

    template_names = [template.name for template in response.templates]

    assert 'links/index.html' in template_names


def count_links(client, url):
    response = client.get(url)
    text = str(response.content)
    links_counter = 0

    for link in re.finditer('single-link', text):
        links_counter = links_counter + 1

    return links_counter


@pytest.mark.django_db
def test_pagination(client, mock_slack_notification):
    mommy.make(Link, _quantity=25)

    links_in_the_first_page = count_links(client, '/links/')

    links_in_the_second_page = count_links(client, '/links/?page=2')

    assert links_in_the_first_page == 20 and links_in_the_second_page == 5


@pytest.mark.django_db
def test_create_link_form_view_response(client):
    response = client.get('/links/create/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_link_form_template_name(client):
    response = client.get('/links/create/')

    template_names = [template.name for template in response.templates]

    assert 'links/create-link-form.html' in template_names


@pytest.mark.django_db
def test_slack_new_link_view_response(client, mock_slack_notification):
    response = client.post('/api/link/', {'text': 'TreeHouse: https://teamtreehouse.com/home',
                                          'user_id': 'U3V3VMPFC'})

    link = Link.objects.all()[0]

    assert response.status_code == 201
    assert link.title == "TreeHouse"
    assert link.url == "https://teamtreehouse.com/home"


@pytest.mark.django_db
def test_slack_new_link_view_refuse_get_method(client, monkeypatch):
    response = client.get('/api/link/')

    assert response.status_code == 405


@pytest.mark.django_db
def test_slack_new_invalid_link_in_view(client):
    response = client.post('/api/link/', {'text': 'TreeHouse:https://teamtreehouse.com/home',
                                          'user_id': 'U3V3VMPFC'})

    assert response.data.get('text') == 'Your Link is not valid.\nPlease check the syntax: title: url'
    assert response.status_code == 400


@pytest.mark.django_db
def test_slack_new_invalid_link_in_link_manager(client):
    with pytest.raises(ValueError):
        Link.objects.create_from_slack('TreeHouse:https://teamtreehouse.com/home', 'U3V3VMPFC')


@pytest.mark.django_db
def test_get_slack_user(client, mock_slack_notification):
    author = get_slack_user('U3V3VMPFC')

    assert author.email == "example@gmail.com"
    assert author.username == "cintia"


@pytest.mark.django_db
def test_create_author(client, mock_slack_notification):
    author = create_author(mommy.make(User))

    assert User.objects.get(id=author.id)


@pytest.mark.django_db
def test_email_sent_from_send_created_user_email(client):
    with patch('django.core.mail.EmailMessage.send') as mocked_send_mail:
        send_created_user_email('123', 'example@gmail.com')

        assert mocked_send_mail.called
