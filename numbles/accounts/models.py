from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from pytz import common_timezones


class Profile(models.Model):
    """
    Storage for user preferences.
    """

    user = models.OneToOneField(
        User,
        primary_key=True
    )

    address = models.TextField(
        blank=True,
        help_text="Used for the business app",
    )

    timezone = models.CharField(
        max_length=40,
        choices=[(t, t) for t in common_timezones],
        default='UTC',
        help_text="Used for displaying all times."
    )

    def __unicode__(self):
        return unicode(self.user)


@receiver(models.signals.post_save, sender=User)
def on_user_save(instance, created, **kwargs):
    """
    Create a Profile instance whenever a user is created.
    """
    if created:
        Profile.objects.create(user=instance)
