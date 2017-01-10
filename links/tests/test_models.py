import pytest
from links.models import Link
from model_mommy import mommy


def has_field(model, field):
    return field in [f.name for f in model._meta.get_fields()]


@pytest.mark.django_db
def test_link_should_have_some_fields():
    assert has_field(Link, 'title')
    assert has_field(Link, 'url')
    assert has_field(Link, 'created')


@pytest.mark.django_db
def test_links_are_ordered_by_date():
    mommy.make(Link, _quantity=10)

    assert set(Link.objects.all()) == set(Link.objects.all().order_by('-created'))
