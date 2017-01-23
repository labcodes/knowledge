import pytest
import re
from model_mommy import mommy
from links.models import Link


@pytest.mark.django_db
def test_index_view_response(client):
    response = client.get('/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_index_template_name(client):
    response = client.get('/')

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

    links_in_the_first_page = count_links(client, '/')

    links_in_the_second_page = count_links(client, '/?page=2')

    assert links_in_the_first_page == 20 and links_in_the_second_page == 5


@pytest.mark.django_db
def test_create_link_form_view_response(client):
    response = client.get('/create-new-link/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_create_link_form_template_name(client):
    response = client.get('/create-new-link/')

    template_names = [template.name for template in response.templates]

    assert 'links/create-link-form.html' in template_names


@pytest.mark.django_db
def test_slack_new_link_view_response(client, mock_slack_notification):
    response = client.post('/api/link/', {'text': 'TreeHouse: https://teamtreehouse.com/home'})

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
    response = client.post('/api/link/', {'text': 'TreeHouse:https://teamtreehouse.com/home'})

    assert response.status_code == 400


@pytest.mark.django_db
def test_slack_new_invalid_link_in_link_manager(client):
    with pytest.raises(ValueError):
        Link.objects.create_from_slack('TreeHouse:https://teamtreehouse.com/home')
