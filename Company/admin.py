from django.contrib import admin
from django.utils.translation import  ugettext_lazy as _
from Company.models import Company , Location,LocationType
from Company import models


class companyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slogan','short_description','long_description','Mission')

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.fk_use = request.user
#         obj.save()

#     def get_queryset(self, request):
#         qs = super(companyAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(fk_use=request.user)

    def has_add_permission(self, request):
        count = Company.objects.all().count()
        if count == 0:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False



class locatioInline(admin.TabularInline):
    model=models.Location
    fields = ('name','fk_locationType','description','Mission','address','phone','email')
    extra = 0

class locationTypeAdmin(admin.ModelAdmin):
    list_display = ('type',)
    inlines = [locatioInline,]
    

admin.site.register(Company, companyAdmin)
admin.site.register(LocationType, locationTypeAdmin)
