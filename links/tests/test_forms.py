from links.forms import LinkForm
from links.models import Link
from links.utils import mock_slack_notification
import pytest


@pytest.mark.usefixtures("mock_slack_notification")
@pytest.mark.django_db
def test_link_creation_valid_form():
    form_data = {'title': 'TreeHouse', 'url': 'https://teamtreehouse.com/home'}
    form = LinkForm(data=form_data)
    form.save()

    assert Link.objects.get(title='TreeHouse', url='https://teamtreehouse.com/home')


def test_link_creation_invalid_form():
    form_data = {'title': 'TreeHouse', 'url': 'Should not pass'}
    form = LinkForm(data=form_data)

    assert not form.is_valid()
