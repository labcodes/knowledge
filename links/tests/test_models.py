import pytest
from links.models import Link
from links.utils import mock_slack_notification
from model_mommy import mommy


@pytest.mark.usefixtures("mock_slack_notification")
@pytest.mark.django_db
def test_create_link():
    link = mommy.make(Link)
    same_link = Link.objects.filter(id=link.id)[0]

    assert link == same_link


@pytest.mark.usefixtures("mock_slack_notification")
@pytest.mark.django_db
def test_links_are_ordered_by_date():
    mommy.make(Link, _quantity=10)

    assert list(Link.objects.all()) == list(Link.objects.all().order_by('-created'))
