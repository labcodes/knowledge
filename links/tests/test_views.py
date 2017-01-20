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
def test_pagination(client):
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
