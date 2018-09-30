from django.utils.translation import  ugettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from Product.models import ProductCategory,Product,Imports,Transfers,Sales,SalesItems
from django.contrib import admin
from django import forms
from Product.views import availableImports, generateInvoice
from Product.views import availableQuantityInLocation
from Company.models import Location
from MyUser.views import availableLocation
import os
from datetime import date
from django.db.models import Sum

"""
*******************************************************************************
*********************************** Product ***********************************
*******************************************************************************
"""

class ProductInline(admin.TabularInline):   
    model = Product 
    fields=('name',  'description','photo','fk_category','displayFlag')
    extra = 0

class CategoryAdmin(admin.ModelAdmin):   
    list_display = ('name',)
    search_fields=['name','Category__name']
    list_filter = ('name',)
    inlines = [ProductInline,]

"""
*******************************************************************************
*********************************** Imports ***********************************
*******************************************************************************
"""

class TransfersInlineValidation(BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        super(TransfersInlineValidation, self).clean()
        totalQuantity = 0
        fk_import_obj = None
        for form in self.forms:
            if not form.is_valid():
                return #other errors exist, so don't bother
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                if form.cleaned_data['the_date'] < self.instance.the_date:    
                    raise ValidationError(_("Transfer Date can't be less than import Date"))
                totalQuantity += form.cleaned_data['quantity']
                if form.cleaned_data['quantity'] == 0:
                    raise ValidationError(_("Can't transfer Zero quantity"))
                    break
            if fk_import_obj is None:
                try:
                    fk_import_obj = form.cleaned_data['fk_import']
                except:
                    raise ValidationError(_('Enter Location and Quantity'))                    
        # to check quantity is less than imported
        if fk_import_obj is not None and fk_import_obj.quantity < totalQuantity:
            raise ValidationError(_('Quantity to transfer is more than imported'))
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
    search_fields=['id','the_date','Imports__fk_location_to','fk_product__name','fk_product__fk_category__name']
    list_filter = ('the_date','Imports__fk_location_to','fk_product__fk_category', 'fk_product')
    inlines = (TransfersInline,)
    fieldsets = (
        (None, {
            'fields': ('fk_product', 'the_date')
        }),
        (_('Import info'), {
            'fields': (('quantity', 'price'),),
        }),
        (_('Selling plan'), {
            'fields': (('selling_price', 'discount_rate'),),
        }),
    )

"""
*******************************************************************************
********************************** Transfers **********************************
*******************************************************************************
"""

class TransfersForm(forms.ModelForm):
    class Meta:
        model = Transfers
        exclude = 0
    
    def clean(self):
        if any(self.errors):
            return 
        fk_import_obj = self.cleaned_data.get('fk_import')
        fk_location_from_obj = self.cleaned_data.get('fk_location_from')
        quantity_obj = self.cleaned_data.get('quantity')
        if quantity_obj == 0:
            raise ValidationError(_("Can't transfer Zero quantity"))
        availableQuantity = availableQuantityInLocation(fk_import_obj, fk_location_from_obj,date.today())
        if self.instance:
            availableQuantity += self.instance.quantity
        if availableQuantity < quantity_obj:
            raise forms.ValidationError(_("This Quantity is not Available, Available Quantity = ") + unicode(availableQuantity))
        return self.cleaned_data

class TransfersAdmin(admin.ModelAdmin):
    form = TransfersForm
    list_display = ('id','fk_import','fk_location_from','fk_location_to','quantity','the_date')
    search_fields=['id','fk_import__id','the_date','fk_location_from__name','fk_location_to__name','fk_import__fk_product__fk_category__name','fk_import__fk_product__name']
    list_filter = ('the_date','fk_location_from','fk_location_to','fk_import__fk_product__fk_category','fk_import__fk_product')
    fieldsets = (
        (None, {
            'fields': ('fk_import', 'the_date')
        }),
        (_('Location'), {
            'fields': (('fk_location_from', 'fk_location_to'),),
        }),
        (_('Quantity'), {
            'fields': ('quantity',),
        }),
    )
    
    def get_queryset(self, request):
        # remove imported data from suppler  (from None)
        qs = super(TransfersAdmin, self).get_queryset(request)
        qs = qs.exclude(fk_location_from__isnull = True)
        return qs

    def render_change_form(self, request, context, *args, **kwargs):
        # get locations can user access
        all_locations = availableLocation(request)
        # show imports that has quantity
        importsIDs = availableImports(all_locations,date.today())
        if context['original'] and context['original'].id:
            importsIDs.append(context['original'].fk_import.id)
        context['adminform'].form.fields['fk_import'].queryset = Imports.objects.filter(id__in = importsIDs)
        return super(TransfersAdmin, self).render_change_form(request, context, args, kwargs)             

"""
*******************************************************************************
************************************ Sales ************************************
*******************************************************************************
"""

class SalesItemInlineValidation(BaseInlineFormSet):

    def clean(self):
        if any(self.errors):
            return
        super(SalesItemInlineValidation, self).clean()
        totalQuantity = 0
        importQuantity = []
        for form in self.forms:
            if not form.is_valid():
                return #other errors exist, so don't bother
            if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                totalQuantity += form.cleaned_data['quantity']
                if form.cleaned_data['quantity'] == 0:
                    raise ValidationError(_("Can't sell Zero quantity"))
                fk_import_obj = form.cleaned_data['fk_import']
                try:
                    fk_location_obj = (form.cleaned_data['fk_sales']).fk_location
                except:
                    raise ValidationError(_("Error"))
                quantity_obj = form.cleaned_data['quantity']
                price_obj = form.cleaned_data['price']
                minPrice = float(fk_import_obj.selling_price * (100 - fk_import_obj.discount_rate))/100
                if minPrice > price_obj:
                    raise ValidationError(_("Can't sale less than ") + unicode(minPrice))
                availableQuantity = availableQuantityInLocation(fk_import_obj, fk_location_obj,date.today())
                if form.cleaned_data['id']:
                    availableQuantity += form.cleaned_data['id'].quantity
                if availableQuantity < quantity_obj:
                    errorMsg = unicode(_('Quantity more than imported for '))
                    errorMsg += unicode(form.cleaned_data['fk_import'].fk_product.__unicode__())
                    errorMsg += unicode(_(' Available Quantity is '))
                    errorMsg += str(availableQuantity)
                    raise ValidationError(errorMsg)
        if totalQuantity <= 0:
            raise ValidationError(_("Can't sell Zero quantity"))
             
        self.instance.__total__ = totalQuantity

class SalesItemInline(admin.TabularInline):
    model = SalesItems
    formset = SalesItemInlineValidation
    fields=('fk_sales','fk_import','quantity','price')
    extra = 0
    
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'fk_import':
            # get locations can user access
            all_locations = availableLocation(request)
            # show imports that has quantity
            importsIDs = availableImports(all_locations,date.today())
            if request.sales:
                sales_imports =  request.sales.Sales.all()
                for i in sales_imports:
                    importsIDs.append(i.fk_import.id)
            kwargs['queryset'] = Imports.objects.filter(id__in = importsIDs)
        return super(SalesItemInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class SalesAdmin(admin.ModelAdmin): 
    list_display = ('id','the_date','fk_location','invoice_link')
    search_fields=['id','the_date','fk_location__name','name','email']
    list_filter = ('the_date','fk_location','Sales__fk_import__fk_product__fk_category','Sales__fk_import__fk_product')

    fieldsets = (
        (None, {
            'fields': ('fk_location', 'the_date')
        }),
        (_('Client Information'), {
            'fields': (('name','phone'), ('address','email')),
        }),
    )
    
    inlines = [SalesItemInline,]
    
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request.sales = obj
        return super(SalesAdmin, self).get_form(request, obj, **kwargs)

    def render_change_form(self, request, context, *args, **kwargs):
        # limit choices of location with location can user access
        all_locations = availableLocation(request)
        context['adminform'].form.fields['fk_location'].queryset = Location.objects.filter(id__in = all_locations)
        return super(SalesAdmin, self).render_change_form(request, context, args, kwargs)             

    def get_queryset(self, request):
        qs = super(SalesAdmin, self).get_queryset(request)
        if request.user.is_superuser: # is super user return all data
            return qs
        # is not super user return sales related to location related to user permission
        return qs.filter(fk_location__in=request.user.fk_locations.all())

    def save_related(self, request, form, formsets, change):
        super(SalesAdmin, self).save_related(request, form, formsets, change)
        obj = form.instance
        # if not obj.id:
        salesItems= []
        total_price = 0
        for form in formsets:
            for salesItem in form.cleaned_data:
                if salesItem and not salesItem.get('DELETE'):
                    total_price += (salesItem['quantity'] * salesItem['price'])
                    salesItems.append({'product':salesItem['fk_import'].fk_product,'quantity':salesItem['quantity'],'price':salesItem['price']})
        invoiceFile = generateInvoice(request, form.instance,salesItems) # generate bill and get file object
        obj.invoice.save(invoiceFile.name,invoiceFile,save=True) # save file 
        os.remove(invoiceFile.name) # remove temp file
        # To Do print
        obj.save()


admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Imports, ImportsAdmin)
admin.site.register(Transfers, TransfersAdmin)
admin.site.register(Sales, SalesAdmin)

# hide add group
from django.contrib.auth.models import Group
admin.site.unregister(Group)

