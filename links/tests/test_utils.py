import pytest
from links.utils import get_title_from_url


@pytest.mark.django_db
def test_get_title_from_url_with_meta_title(client):
    assert get_title_from_url('https://api.slack.com/') == 'Slack API'


@pytest.mark.django_db
def test_get_title_from_url_without_meta_title(client):
    assert get_title_from_url('https://teamtreehouse.com/home') == 'Treehouse | Sign In'
