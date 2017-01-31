import pytest
from links.utils import get_title_from_url, check_for_http_in_url


@pytest.mark.django_db
def test_get_title_from_url_with_meta_title(client):
    assert get_title_from_url('https://api.slack.com/') == 'Slack API'


@pytest.mark.django_db
def test_get_title_from_url_without_meta_title(client):
    assert get_title_from_url('https://teamtreehouse.com/home') == 'Treehouse | Sign In'


@pytest.mark.django_db
def test_check_for_http_in_url_with_http_in_url(client):
    assert check_for_http_in_url('https://api.slack.com/') == 'https://api.slack.com/'


@pytest.mark.django_db
def test_check_for_http_in_url_without_http_in_url(client):
    assert check_for_http_in_url('api.slack.com/') == 'http://api.slack.com/'
