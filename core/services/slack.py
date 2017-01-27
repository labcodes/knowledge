from slackclient import SlackClient
from knowledge.settings import SLACK_TOKEN, SLACK_CHANNEL_ID, SLACK_BOT_NAME


def send_notification_to_slack(link):

    sc = SlackClient(SLACK_TOKEN)
    sc.api_call('chat.postMessage', channel=SLACK_CHANNEL_ID, text=link.url,
        username=SLACK_BOT_NAME, icon_emoji=':information_desk_person:', unfurl_links=True)
