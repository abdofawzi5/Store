from django.contrib import admin
from django.utils.translation import  ugettext_lazy as _
from Website.models import Message

class MessageAdmin(admin.ModelAdmin):    
    list_display = ('the_date','name', 'email','phone',)
    search_fields=['name','the_date','email','phone']
    list_filter = ('the_date',)
    readonly_fields=('the_date','name', 'email','phone','message',)
    fieldsets = (
        (None, {
            'fields': ('the_date',)
        }),
        (_('From'), {
            'fields': (('name', 'email','phone'),),
        }),
        (_('Message'), {
            'fields': ('message',),
        }),
    )

    def has_add_permission(self, request):
        return False

admin.site.register(Message,MessageAdmin)