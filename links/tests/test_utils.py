import pytest
from links.utils import (get_title_from_url, ensure_http_prefix, text_has_tag,
    get_url_from_text, get_tags_from_text)


@pytest.mark.django_db
def test_get_title_from_url_with_meta_title(client):
    assert get_title_from_url('https://api.slack.com/') == 'Slack API'


@pytest.mark.django_db
def test_get_title_from_url_without_meta_title(client):
    assert get_title_from_url('https://teamtreehouse.com/home') == 'Treehouse | Sign In'


@pytest.mark.django_db
def test_ensure_http_prefix_with_http_in_url(client):
    assert ensure_http_prefix('https://api.slack.com/') == 'https://api.slack.com/'


@pytest.mark.django_db
def test_ensure_http_prefix_without_http_in_url(client):
    assert ensure_http_prefix('api.slack.com/') == 'http://api.slack.com/'


def test_text_has_tag_including_text_with_tags(client):
    assert text_has_tag('https://api.slack.com/ api, slack')


def test_text_has_tag_including_text_without_tags(client):
    assert not text_has_tag('https://api.slack.com/')


def test_get_url_from_text_including_text_with_tags(client):
    assert get_url_from_text('https://api.slack.com/ api, slack') == 'https://api.slack.com/'


def test_get_url_from_text_including_text_without_tags(client):
    assert get_url_from_text('https://api.slack.com/') == 'https://api.slack.com/'


def test_get_tags_from_text_including_text_with_tags(client):
    assert get_tags_from_text('https://api.slack.com/ api, slack') == 'api, slack'


def test_get_tags_from_text_including_text_without_tags(client):
    assert get_tags_from_text('https://api.slack.com/') == ''
