from __future__ import unicode_literals
from django.utils.translation import  ugettext_lazy as _

from django.db import models
from datetime import datetime

SHORT_NAME_LENGTH = 20
LONG_NAME_LENGTH = 50
SHORT_TEXT_LENGTH = 100
LONG_TEXT_LENGTH = 800

class Message(models.Model):
    name = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name = _('Name'))
    email = models.EmailField(verbose_name = _('Email'))
    phone = models.CharField(max_length = LONG_NAME_LENGTH, verbose_name = _('Phone'))
    message = models.CharField(max_length = LONG_TEXT_LENGTH, verbose_name = _('Message'))
    the_date = models.DateTimeField(default=datetime.now,verbose_name = _('Date and Time'))
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

class Advertisement(models.Model):
    name = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name = _('Name'))
    photo = models.ImageField(upload_to = 'Advertisement/' ,verbose_name = _('photo'),help_text = _('800x300'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('advertisement')
        verbose_name_plural = _('Advertisements')

class Post(models.Model):
    title = models.CharField(max_length = LONG_NAME_LENGTH, verbose_name = _('Title'))
    detail = models.CharField(max_length = SHORT_TEXT_LENGTH, verbose_name = _('Detail'))
    the_date = models.DateTimeField(default=datetime.now,verbose_name = _('Date and Time'))

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        
