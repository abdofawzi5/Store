from django.utils.translation import  ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from Company.models import Location

class User(AbstractUser):
    fk_locations = models.ManyToManyField(Location,verbose_name = _('access Location'),related_name = _('accessLocation'),help_text = _('Locations can access and edit'),blank = True, null = True)
