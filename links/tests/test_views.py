import pytest


@pytest.mark.django_db
def test_index_view_response(client):
    response = client.get('/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_index_template_name(client):
    response = client.get('/')

    template_names = [template.name for template in response.templates]

    assert 'links/index.html' in template_names
