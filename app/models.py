from django.db import models
from django.contrib.auth.models import User

class MetaInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True

# Facebook user attached to steemit username
class FacebookUser(MetaInfo):
    steem_username = models.CharField(max_length=50, blank=True)
    messenger_id = models.BigIntegerField(default=0, unique=True)

    class Meta:
        verbose_name = "Facebook User"
        verbose_name_plural = "Facebook Users"

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.gender)