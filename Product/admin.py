from django.utils.translation import  ugettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Q
from Product.models import Category,Product,Imports,Transfers,Sales
from django.contrib import admin
from django import forms
from django.db.models.functions import Coalesce
from django.db.models.aggregates import Sum

class ProductInline(admin.TabularInline):   
    model = Product 
    fields=('name',  'description', 'price','photo','fk_category')
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
            if fk_import_obj is None:
                fk_import_obj = form.cleaned_data['fk_import']
        # to check quantity is less than imported
        if fk_import_obj.quantity < totalQuantity:
            raise ValidationError(_('Quantity in Locations more than imported'))
        self.instance.__total__ = totalQuantity

class TransfersInline(admin.TabularInline):
    model = Transfers
    formset = TransfersInlineValidation
    fields=('fk_import','fk_location_to','quantity', 'price','discount_rate','the_date')
    extra = 0
    
    def get_queryset(self, request):
        qs = super(TransfersInline, self).get_queryset(request)
        # display just transfers made from imports
        qs = qs.filter(fk_location_from = None)
        return qs

class ImportsAdmin(admin.ModelAdmin):   
    list_display = ('id','fk_product','quantity','price','the_date')
    inlines = (TransfersInline,)

class TransfersForm(forms.ModelForm):
    class Meta:
        model = Transfers
        exclude = 0
    
    def clean(self):
        fk_import_obj = self.cleaned_data.get('fk_import')
        fk_location_from_obj = self.cleaned_data.get('fk_location_from')
        quantity_obj = self.cleaned_data.get('quantity')
        
        totalTransferred = Transfers.objects.filter(Q(fk_location_from = fk_location_from_obj)|Q(fk_location_to = fk_location_from_obj),fk_import=fk_import_obj)
        availableQuantity = 0
        totalTransferred_in_ids = []
        for oneTransfer in totalTransferred:
            if oneTransfer.fk_location_from == fk_location_from_obj:
                availableQuantity -= oneTransfer.quantity
            if oneTransfer.fk_location_to == fk_location_from_obj:
                availableQuantity += oneTransfer.quantity
                totalTransferred_in_ids.append(oneTransfer.id)
        soldQuantity = Sales.objects.filter(fk_transfer__in = totalTransferred_in_ids).aggregate(soldQuantity = Coalesce(Sum('quantity'),0))['soldQuantity']
        availableQuantity -= soldQuantity
        if availableQuantity < quantity_obj:
            raise forms.ValidationError(_("This Quantity is not Available, Available Quantity = ") + unicode(availableQuantity))
        return self.cleaned_data

class TransfersAdmin(admin.ModelAdmin):   
    form = TransfersForm
    list_display = ('id','fk_import','fk_location_from','fk_location_to','quantity','price','discount_rate','the_date')

    def get_queryset(self, request):
        # remove imported data from suppler  (from None)
        qs = super(TransfersAdmin, self).get_queryset(request)
        qs = qs.exclude(fk_location_from__isnull = True)
        return qs


class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        exclude = 0

    def clean(self):
        price_obj = self.cleaned_data.get('price')
        quantity_obj = self.cleaned_data.get('quantity')
        fk_transfer_obj = self.cleaned_data.get('fk_transfer')
        minPrice = float(fk_transfer_obj.price * (100 - fk_transfer_obj.discount_rate))/100
        availableQuantity = fk_transfer_obj.quantity - Sales.objects.filter(fk_transfer=fk_transfer_obj).aggregate(soldQuantity = Coalesce(Sum('quantity'),0))['soldQuantity']
        if quantity_obj > availableQuantity:
            raise forms.ValidationError(_("This Quantity is not Available, Available Quantity = ") + unicode(availableQuantity))
        if quantity_obj == 0:
            raise forms.ValidationError(_("You can't sell Zero quantity"))
        if price_obj < minPrice:
            raise forms.ValidationError(_("Can't sale less than ") + unicode(minPrice))
        return self.cleaned_data


class SalesAdmin(admin.ModelAdmin): 
    form = SalesForm  
    list_display = ('fk_transfer','quantity','price','the_date','bill')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Imports, ImportsAdmin)
admin.site.register(Transfers, TransfersAdmin)
admin.site.register(Sales, SalesAdmin)


