from django.db import models
from core.services.slack import send_notification_to_slack


class LinkManager(models.Manager):

    def create_from_slack(self, slack_text):
        title, url = slack_text.split(': ')
        return self.create(title=title, url=url)


class Link(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    objects = LinkManager()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            send_notification_to_slack(self)

        super(Link, self).save(*args, **kwargs)
