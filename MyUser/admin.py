from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import  ugettext_lazy as _
from MyUser.models import User

class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'fk_locations',
#                                         'groups', 'user_permissions'
                                       )}),
#         (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('fk_locations','groups', 'user_permissions')
    
admin.site.register(User, MyUserAdmin)
