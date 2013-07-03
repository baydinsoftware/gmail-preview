
from django.db import models
from django.contrib.auth.models import User


class Preview(models.Model):

    """ Preview information of an email. 

    Add last_updated field??

    """

    sender = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    body = models.CharField(max_length=480)
    date = models.DateTimeField()
    creator = models.ForeignKey(User)

    def __unicode__(self):
        return self.subject


class Comment(models.Model):
    """ Stores comments on a preview. """
    
    preview = models.ForeignKey(Preview)
    comment = models.CharField(max_length=480)
    date = models.DateTimeField()
    commentor = models.ForeignKey(User)

    def __unicode__(self):
        return self.comment
