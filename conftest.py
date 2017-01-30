import pytest
import slackclient


@pytest.fixture
def mock_slack_notification(monkeypatch):
    def mock_fake_response_from_slack(*args, **kwargs):
        return {'profile': {'email': 'example@gmail.com', 'first_name': 'Cintia'}}

    monkeypatch.setattr(slackclient.SlackClient, 'api_call', mock_fake_response_from_slack)
