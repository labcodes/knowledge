from django.contrib.auth.models import User, BaseUserManager
from slackclient import SlackClient
from knowledge.settings import SLACK_TOKEN, SLACK_CHANNEL_ID, SLACK_BOT_NAME
from .utils import send_created_user_email


def send_notification_to_slack(link):
    text_formatted = "{} enviou:\n {}".format(link.author, link.url)

    sc = SlackClient(SLACK_TOKEN)
    sc.api_call('chat.postMessage', channel=SLACK_CHANNEL_ID, text=text_formatted,
        username=SLACK_BOT_NAME, icon_emoji=':information_desk_person:', unfurl_links=True)


def create_author(user):
    password = BaseUserManager().make_random_password()
    user.set_password(password)
    user.save()
    send_created_user_email(password, user.email)

    return user


def get_slack_user(slack_user_id):
    sc = SlackClient(SLACK_TOKEN)

    profile = sc.api_call('users.profile.get', user=slack_user_id).get('profile')
    email = profile.get('email')
    username = profile.get('first_name').lower()

    user, created = User.objects.get_or_create(email=email, is_superuser=True, username=username, is_staff=True)

    if created:
        user = create_author(user)

    return user
