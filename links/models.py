from django.contrib.auth.models import User
from django.db import models

from core.services.slack import send_notification_to_slack, get_slack_user
from links.utils import get_title_from_url, ensure_http_prefix, get_tags_from_text

from tagging.models import TagManager
from tagging.fields import TagField


class LinkManager(models.Manager):

    def create_from_slack(self, text, slack_url, slack_user_id):
        tags = get_tags_from_text(text)
        title = get_title_from_url(slack_url)
        author = get_slack_user(slack_user_id)
        slack_url = ensure_http_prefix(slack_url)

        return self.create(title=title, url=slack_url, author=author, tags=tags)


class Link(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='links', null=True)
    tags = TagField()

    objects = LinkManager()
    tags_manager = TagManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.title:
                self.title = get_title_from_url(self.url)
            send_notification_to_slack(self)

        super(Link, self).save(*args, **kwargs)
