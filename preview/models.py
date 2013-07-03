
from django.db import models


class Preview(models.Model):

    """ Preview information of an email. 

    Add last_updated field??

    """

    sender = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    body = models.CharField(max_length=480)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.subject

class Comment(models.Model):
    """ Stores comments on a preview.

    Need to add user field - how does this get hooked into the 
    authentication system? 

    """
    
    ## change this field to 'preview' - sync tables
    preview = models.ForeignKey(Preview)
    comment = models.CharField(max_length=480)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.comment
