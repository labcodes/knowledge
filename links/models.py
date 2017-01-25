from django.contrib.auth.models import User
from django.db import models
from links.services.slack import get_slack_user


class LinkManager(models.Manager):

    def create_from_slack(self, slack_text, slack_user_id):
        title, url = slack_text.split(': ')
        author = get_slack_user(slack_user_id)

        return self.create(title=title, url=url, author=author)


class Link(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='links', null=True)

    objects = LinkManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            send_notification_to_slack(self)

        super(Link, self).save(*args, **kwargs)
