from django.contrib import admin
from django.utils.translation import  ugettext_lazy as _
from Website.models import Message, Advertisement, Post
from django import forms

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

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo',)

class PostModelForm( forms.ModelForm ):
    model = Post
    detail = forms.CharField( widget=forms.Textarea )
    
class PostAdmin(admin.ModelAdmin):
    form = PostModelForm
    list_display = ('title',)
    readonly_fields=('the_date',)

admin.site.register(Message,MessageAdmin)
admin.site.register(Advertisement,AdvertisementAdmin)
admin.site.register(Post,PostAdmin)
