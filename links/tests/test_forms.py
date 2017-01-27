from links.forms import LinkForm
from links.models import Link
import pytest


@pytest.mark.django_db
def test_link_creation_valid_form(mock_slack_notification):
    form_data = {'url': 'https://api.slack.com/'}
    form = LinkForm(data=form_data)
    form.save()

    link = Link.objects.get(url='https://api.slack.com/')

    assert link.url == 'https://api.slack.com/'
    assert link.title == "Slack API"


def test_link_creation_invalid_form():
    form_data = {'url': 'Should not pass'}
    form = LinkForm(data=form_data)

    assert not form.is_valid()
