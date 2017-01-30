import pytest
from core.services.slack import get_slack_user, create_author
from links.utils import get_title_from_url
from core.services.utils import send_created_user_email
from unittest.mock import patch
from model_mommy import mommy
from django.contrib.auth.models import User


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
def test_get_title_from_url_with_meta_title(client):
    assert get_title_from_url('https://api.slack.com/') == 'Slack API'


@pytest.mark.django_db
def test_get_title_from_url_without_meta_title(client):
    assert get_title_from_url('https://teamtreehouse.com/home') == 'Treehouse | Sign In'


@pytest.mark.django_db
def test_email_sent_from_send_created_user_email(client):
    with patch('django.core.mail.EmailMessage.send') as mocked_send_mail:
        send_created_user_email('123', 'example@gmail.com')

        assert mocked_send_mail.called
