from django.contrib.auth.models import User
from slackclient import SlackClient
from knowledge.settings import SLACK_TOKEN, SLACK_CHANNEL_ID, SLACK_BOT_NAME


def send_notification_to_slack(link):
    text_formatted = "{} enviou:\n{}\n{}".format(link.author, link.title, link.url)

    sc = SlackClient(SLACK_TOKEN)
    sc.api_call('chat.postMessage', channel=SLACK_CHANNEL_ID, text=text_formatted,
        username=SLACK_BOT_NAME, icon_emoji=':information_desk_person:')


def get_slack_user(slack_user_id):
    sc = SlackClient(SLACK_TOKEN)

    profile = sc.api_call('users.profile.get', user=slack_user_id).get('profile')
    email = profile.get('email')
    username = profile.get('first_name').lower()

    user, created = User.objects.get_or_create(email=email, is_superuser=True, username=username, is_staff=True)

    return user, created
