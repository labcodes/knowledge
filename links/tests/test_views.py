import pytest
import re
from django.contrib.auth.models import User
from model_mommy import mommy
from links.models import Link


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
    user = User.objects.create_user(username='testuser', password='12345')

    user.save()

    login = client.login(username='testuser', password='12345')

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

    assert response.data.get('text') == 'Your Link is not valid.\nPlease check the syntax: title: url'
    assert response.status_code == 400


@pytest.mark.django_db
def test_slack_new_invalid_link_in_link_manager(client):
    with pytest.raises(ValueError):
        Link.objects.create_from_slack('TreeHouse:https://teamtreehouse.com/home', 'U3V3VMPFC')


@pytest.mark.django_db
def test_valid_login_view(client):
    user = mommy.make(User)
    response = client.post('/links/login/', {'username': user.email,
                                             'password': user.password})

    assert response.status_code == 200


@pytest.mark.django_db
def test_invalid_login_view(client):
    response = client.post('/links/login/', {'username': 'Error',
                                             'password': 'Error'})
    assert response.context['login_error'] == 'Wrong email or password'
