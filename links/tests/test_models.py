import pytest
from links.models import Link
from model_mommy import mommy


@pytest.mark.django_db
def test_create_link(mock_slack_notification):
    link = mommy.make(Link)
    same_link = Link.objects.filter(id=link.id)[0]

    assert link == same_link


@pytest.mark.django_db
def test_create_from_slack_link_manager(mock_slack_notification):

    text = "https://api.slack.com/"
    link = Link.objects.create_from_slack(text)

    assert link.title == "Slack API"
    assert link.url == "https://api.slack.com/"


@pytest.mark.django_db
def test_links_are_ordered_by_date(mock_slack_notification):
    mommy.make(Link, _quantity=10)

    assert list(Link.objects.all()) == list(Link.objects.all().order_by('-created'))
