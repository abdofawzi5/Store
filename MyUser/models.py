from django.utils.translation import  ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from Company.models import Location

class User(AbstractUser):
    fk_locations = models.ManyToManyField(Location,verbose_name = _('access Location'),related_name = _('accessLocation'),help_text = _('Locations can access and edit'),blank = True)

    def save(self, *args, **kwargs):
        super(User, self).save(*args,**kwargs)
        self.is_staff = True
        permission = Permission.objects.get(codename = 'add_sales')
        self.user_permissions.add(permission)      
        permission = Permission.objects.get(codename = 'change_sales')
        self.user_permissions.add(permission)      
        permission = Permission.objects.get(codename = 'add_salesitems')
        self.user_permissions.add(permission)      
        permission = Permission.objects.get(codename = 'change_salesitems')
        self.user_permissions.add(permission)      
        return super(User, self).save(*args,**kwargs)