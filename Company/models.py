from django.db import models
from django.utils.translation import  ugettext_lazy as _

SHORT_NAME_LENGTH = 40
LONG_NAME_LENGTH = 50
SHORT_TEXT_LENGTH = 100
LONG_TEXT_LENGTH = 800



class Company(models.Model):
    name = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name = _('Company Name'))
    logo = models.ImageField(blank = True, null = True,upload_to = 'company_logo/' , verbose_name = _('Logo'))
    slogan = models.CharField(blank = True, null = True,max_length = LONG_NAME_LENGTH, verbose_name = _('Slogan'))
    short_description = models.CharField(blank = True, null = True,max_length = SHORT_TEXT_LENGTH, verbose_name = _('Short Description'))
    long_description = models.CharField(blank = True, null = True,max_length = LONG_TEXT_LENGTH, verbose_name = _('Long Description'))
    Mission = models.CharField(blank = True, null = True,max_length = LONG_TEXT_LENGTH, verbose_name = _('Mission'))
    phone = models.CharField(max_length = LONG_NAME_LENGTH, verbose_name = _('Phone'))
    address = models.CharField(max_length = LONG_NAME_LENGTH, verbose_name = _('Address'))
    email = models.EmailField(blank = True, null = True,verbose_name = _('Email'))
    facebook = models.URLField(blank = True, null = True,verbose_name = _('Facebook'))
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

class LocationType(models.Model):
    type = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name = _('Location Type'))

    def __unicode__(self):
        return unicode(self.type) 

    class Meta:
        verbose_name = _('Location Type')
        verbose_name_plural = _('Location Types')

class Location(models.Model):
    fk_locationType = models.ForeignKey(LocationType ,verbose_name = _('Location Type'))
    name = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name=_('Name'))
    photo = models.ImageField(blank = True, null = True ,upload_to = 'location_logo/' ,verbose_name = _('photo'))
    description = models.CharField(blank = True, null = True,max_length = SHORT_TEXT_LENGTH, verbose_name = _('Short Description'))
    Mission = models.CharField(blank = True, null = True ,max_length = LONG_TEXT_LENGTH, verbose_name = _('Mission'))
    createdAt = models.DateField(auto_now_add=True , verbose_name = _('Created At'))
    phone = models.CharField(max_length = LONG_NAME_LENGTH, verbose_name = _('Phone'))
    address = models.CharField(max_length = LONG_NAME_LENGTH, verbose_name = _('Address'))
    email = models.EmailField(blank = True, null = True,verbose_name = _('Email'))

    def __unicode__(self):
        return unicode(self.fk_locationType) + '-' + unicode(self.name)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
