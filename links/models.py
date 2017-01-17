from django.db import models
from slackclient import SlackClient
from knowledge.settings import SLACK_TOKEN, SLACK_BOT_NAME, SLACK_CHANNEL_ID

# Create your models here.


class Link(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            textFormatted = "{}\n{}".format(self.title, self.url)

            sc = SlackClient(SLACK_TOKEN)
            sc.api_call('chat.postMessage', channel=SLACK_CHANNEL_ID, text=textFormatted,
                username=SLACK_BOT_NAME, icon_emoji=':information_desk_person:')

            # close slack api?
        super(Link, self).save(*args, **kwargs)
