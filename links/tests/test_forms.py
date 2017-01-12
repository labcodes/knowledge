from links.forms import LinkForm


def test_link_creation_valid_form():
    form_data = {'title': 'TreeHouse', 'url': 'https://teamtreehouse.com/home'}
    form = LinkForm(data=form_data)
    assert form.is_valid()


def test_link_creation_invalid_form():
    form_data = {'title': 'TreeHouse', 'url': 'Should not pass'}
    form = LinkForm(data=form_data)

    assert not form.is_valid()
