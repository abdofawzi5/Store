from django.utils.translation import  ugettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Q
from Product.models import ProductCategory,Product,Imports,Transfers,Sales
from django.contrib import admin
from django import forms
from django.db.models.functions import Coalesce
from django.db.models.aggregates import Sum
from Product.views import availableQuantityInLocation, availableImportsIDs
from Company.models import Location

class ProductInline(admin.TabularInline):   
    model = Product 
    fields=('name',  'description','photo','fk_category')
    extra = 0

class CategoryAdmin(admin.ModelAdmin):   
    list_display = ('name',)
    inlines = [ProductInline,]

class TransfersInlineValidation(BaseInlineFormSet):
    def clean(self):
        super(TransfersInlineValidation, self).clean()
        totalQuantity = 0
        fk_import_obj = None
        for form in self.forms:
            if not form.is_valid():
                return #other errors exist, so don't bother
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                totalQuantity += form.cleaned_data['quantity']
                if form.cleaned_data['quantity'] == 0:
                    raise ValidationError(_("Can't transfer Zero quantity"))
                    break
            if fk_import_obj is None:
                fk_import_obj = form.cleaned_data['fk_import']
                    
        # to check quantity is less than imported
        if fk_import_obj is not None and fk_import_obj.quantity < totalQuantity:
            raise ValidationError(_('Quantity in Locations more than imported'))
        self.instance.__total__ = totalQuantity

class TransfersInline(admin.TabularInline):
    model = Transfers
    formset = TransfersInlineValidation
    fields=('fk_import','fk_location_to','quantity','the_date')
    extra = 0
    
    def get_queryset(self, request):
        qs = super(TransfersInline, self).get_queryset(request)
        # display just transfers made from imports
        qs = qs.filter(fk_location_from = None)
        return qs

class ImportsAdmin(admin.ModelAdmin):
    list_display = ('id','the_date','fk_product','quantity','price','selling_price','discount_rate')
    inlines = (TransfersInline,)

class TransfersForm(forms.ModelForm):
    class Meta:
        model = Transfers
        exclude = 0
    
    def clean(self):
        fk_import_obj = self.cleaned_data.get('fk_import')
        fk_location_from_obj = self.cleaned_data.get('fk_location_from')
        quantity_obj = self.cleaned_data.get('quantity')
        if quantity_obj == 0:
            raise ValidationError(_("Can't transfer Zero quantity"))
        availableQuantity = availableQuantityInLocation(fk_import_obj, fk_location_from_obj)
        if availableQuantity < quantity_obj:
            raise forms.ValidationError(_("This Quantity is not Available, Available Quantity = ") + unicode(availableQuantity))
        return self.cleaned_data

class TransfersAdmin(admin.ModelAdmin):
    form = TransfersForm
    list_display = ('id','fk_import','fk_location_from','fk_location_to','quantity','the_date')

    def get_queryset(self, request):
        # remove imported data from suppler  (from None)
        qs = super(TransfersAdmin, self).get_queryset(request)
        qs = qs.exclude(fk_location_from__isnull = True)
        return qs


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        exclude = 0

    def __init__(self, *args, **kwargs):
        # to add request to form
        self.request = kwargs.pop('request', None)
        super(SalesForm, self).__init__(*args, **kwargs)

    def clean(self):
        fk_import_obj = self.cleaned_data.get('fk_import')
        fk_location_obj = self.cleaned_data.get('fk_location')
        price_obj = self.cleaned_data.get('price')
        quantity_obj = self.cleaned_data.get('quantity')
        if fk_location_obj not in self.request.user.fk_locations.all() and self.request.user.is_superuser == False:
            raise forms.ValidationError(_("You don't have permission to add sales to this location"))
        
        if quantity_obj == 0:
            raise forms.ValidationError(_("Can't sell Zero quantity"))
            
        availableQuantity = availableQuantityInLocation(fk_import_obj, fk_location_obj)
        if quantity_obj > availableQuantity:
            raise forms.ValidationError(_("This Quantity is not Available, Available Quantity = ") + unicode(availableQuantity))
     
        minPrice = float(fk_import_obj.selling_price * (100 - fk_import_obj.discount_rate))/100
        if price_obj < minPrice:
            raise forms.ValidationError(_("Can't sale less than ") + unicode(minPrice))
        
        return self.cleaned_data

class SalesAdmin(admin.ModelAdmin): 
    form = SalesForm
    list_display = ('id','the_date','fk_import','fk_location','quantity','price')

    def render_change_form(self, request, context, *args, **kwargs):
        all_locations = None
        if request.user.is_superuser == False:
            # limit choices of location with locations can user access
            all_locations = request.user.fk_locations.all()
            context['adminform'].form.fields['fk_location'].queryset = Location.objects.filter(id__in = all_locations)
        else:
            all_locations = Location.objects.all()
        # limit choices of imports with imports have quantity in each location
        importsIDs = []
        for one_location in all_locations:     
            importsIDs += availableImportsIDs(one_location)
        context['adminform'].form.fields['fk_import'].queryset = Imports.objects.filter(id__in = importsIDs)
        return super(SalesAdmin, self).render_change_form(request, context, args, kwargs)             

    # add request key to self to access request in forms
    def get_form(self, request, obj=None, **kwargs):
        AdminForm = super(SalesAdmin, self).get_form(request, obj, **kwargs)
        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)
        return AdminFormWithRequest

    def get_queryset(self, request):
        qs = super(SalesAdmin, self).get_queryset(request)
        if request.user.is_superuser: # is super user return all data
            return qs
        # is not super user return sales related to location related to user permission
        return qs.filter(fk_location__in=request.user.fk_locations.all())


admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Imports, ImportsAdmin)
admin.site.register(Transfers, TransfersAdmin)
admin.site.register(Sales, SalesAdmin)

# hide add group
from django.contrib.auth.models import Group
admin.site.unregister(Group)

