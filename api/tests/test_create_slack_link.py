import pytest
from unittest.mock import patch
from model_mommy import mommy
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_valid_payload(client):    
    client = APIClient()
    with patch('links.models.LinkManager.create_from_slack') as mocked_create:
        response = client.post(
            '/api/link/',
            {'text': 'http://google.com', 'user_id': 'dummy'},
            format='json'
        )
        mocked_create.assert_called_once()
        assert response.status_code == 201
