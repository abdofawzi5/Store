from django.utils.translation import  ugettext_lazy as _
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

class ImportsAdmin(admin.ModelAdmin):   
    list_display = ('fk_product','fk_location_to','quantity','price','the_date')


class TransfersForm(forms.ModelForm):
    class Meta:
        model = Transfers
        exclude = 0
    
    def clean(self):
        fk_import_obj = self.cleaned_data.get('fk_import')
        fk_location_from_obj = self.cleaned_data.get('fk_location_from')
        quantity_obj = self.cleaned_data.get('quantity')
        availableQuantity = fk_import_obj.quantity - Transfers.objects.filter(fk_import = fk_import_obj).aggregate(transferredQuantity = Coalesce(Sum('quantity'),0))['transferredQuantity']
        if fk_import_obj.fk_location_to != fk_location_from_obj:
            raise forms.ValidationError(_("This Location to transfer to not has chosen import, This import is in ")+ unicode(fk_import_obj.fk_location_to))
        if quantity_obj > availableQuantity:
            raise forms.ValidationError(_("This Quantity is not Available, Available Quantity = ") + unicode(availableQuantity))
        return self.cleaned_data

class TransfersAdmin(admin.ModelAdmin):   
    form = TransfersForm
    list_display = ('fk_import','fk_location_from','fk_location_to','quantity','price','discount_rate','the_date')

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        exclude = 0

    def clean(self):
        price_obj = self.cleaned_data.get('price')
        quantity_obj = self.cleaned_data.get('quantity')
        fk_transfer_obj = self.cleaned_data.get('fk_transfer')
        print self.cleaned_data
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


