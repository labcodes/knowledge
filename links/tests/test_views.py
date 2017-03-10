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
    user = User.objects.create_user(username='test', password='12345', email="example@gmail.com")

    user.save()

    return client.login(username='example@gmail.com', password='12345')


@pytest.mark.django_db
def test_list_links_view_response(client):
    login = log_user_in(client)

    response = client.get('/links/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_list_links_template_name(client):
    login = log_user_in(client)

    response = client.get('/links/')

    template_names = [template.name for template in response.templates]

    assert 'links/index.html' in template_names


def count_links(client, url):
    response = client.get(url)
    text = str(response.content)
    links_counter = 0

    for link in re.finditer('link-panel-js', text):
        links_counter = links_counter + 1

    return links_counter


@pytest.mark.django_db
def test_pagination(client, mock_slack_notification):
    login = log_user_in(client)

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


@pytest.mark.django_db
def test_tag_that_does_not_exist(client):
    login = log_user_in(client)

    response = client.get('/links/?tag=tagdoesnotexist')

    assert len(response.context['links']) == 0


@pytest.mark.django_db
def test_tag_that_does_exist(client):
    login = log_user_in(client)

    tag = Tag.objects.create(name="test_tag")

    link = mommy.make(Link)
    link.tags = tag.name
    link.save()

    response = client.get('/links/?tag=test_tag')

    assert len(response.context['links']) == 1
