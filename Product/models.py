from django.db import models
from django.utils.translation import  ugettext_lazy as _
from Company.models import Location
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from django.dispatch import receiver

SHORT_NAME_LENGTH = 20
LONG_NAME_LENGTH = 50
SHORT_TEXT_LENGTH = 100
LONG_TEXT_LENGTH = 800

class ProductCategory(models.Model):
    name = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name=_('Category'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

class Product(models.Model):
    name = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name=_('Product Name'))
    photo = models.ImageField(blank = True, null = True ,upload_to = 'Product/' ,verbose_name = _('photo'))
    description = models.CharField(blank = True, null = True,max_length = LONG_TEXT_LENGTH, verbose_name = _('Description'))
    fk_category = models.ForeignKey(ProductCategory, verbose_name=_('Category'))
    createdAt = models.DateField(auto_now_add=True , verbose_name = _('Created At'))

    def __unicode__(self):
        return unicode(self.fk_category) + '-' + unicode(self.name)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Imports(models.Model):
    fk_product = models.ForeignKey(Product, verbose_name = _('Product Product'),related_name = _('Product'))
    quantity = models.IntegerField(default=0,validators = [MinValueValidator(0)], verbose_name=_('Quantity'))
    price = models.FloatField(blank=True,null=True,validators = [MinValueValidator(0.0)],default=0 ,verbose_name=_('Total Price'))
    selling_price = models.FloatField(default=0,validators = [MinValueValidator(0.0)] ,verbose_name=_('Selling Price per Item')) 
    discount_rate = models.FloatField(default=0,validators = [MinValueValidator(0.0), MaxValueValidator(10.0)] ,verbose_name=_('Discount Rate'))
    the_date = models.DateField(default=date.today ,blank=False, verbose_name = _('Date'))
    
    def __unicode__(self):
        return str(self.id) +'-'+unicode(self.fk_product) +'-IM'+ str(self.the_date.year)+ str(self.the_date.month)+ str(self.the_date.day)
    
    class Meta:
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')



class Transfers(models.Model):
    fk_import = models.ForeignKey(Imports, verbose_name = _('Imports'),related_name = _('Imports'))
    fk_location_from = models.ForeignKey(Location, null = True, verbose_name = _('Transfer From'),related_name = _('TransferFrom'))
    fk_location_to = models.ForeignKey(Location, verbose_name=_('Transfer To'),related_name = _('TransferTo'))
    quantity = models.IntegerField(default=0,validators = [MinValueValidator(0)], verbose_name=_('Quantity'))
    the_date = models.DateField(default=date.today ,blank=False, verbose_name = _('Date'))
    
    def __unicode__(self):
        return unicode(self.fk_import) +'-T'+ str(self.the_date.year)+ str(self.the_date.month)+ str(self.the_date.day)
    
    class Meta:
        verbose_name = _('Transfer')
        verbose_name_plural = _('Transfers')

class Sales(models.Model):
    fk_location = models.ForeignKey(Location, verbose_name = _('Location'),related_name = _('Location'))
    the_date = models.DateField(default=date.today ,blank=False, verbose_name = _('Date'))
    invoice = models.FileField(upload_to = 'invoices/',editable=False ,verbose_name = _('invoice'))

    def __unicode__(self):
        return str(self.id) +'-'+unicode(self.fk_location)+'-S'+ str(self.the_date.year)+ str(self.the_date.month)+ str(self.the_date.day)
    
    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')

    def invoice_link(self):
        if self.invoice:
            return "<a href='%s'>Download invoice</a>" % (self.invoice.url,)
        else:
            return "No attachment"
    invoice_link.allow_tags = True

# These two auto-delete files from filesystem when they are unneeded:
@receiver(models.signals.post_delete, sender=Sales)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from file system
    when corresponding `Sales` object is deleted.
    """
    if instance.invoice:
        if os.path.isfile(instance.invoice.path):
            os.remove(instance.invoice.path)

@receiver(models.signals.pre_save, sender=Sales)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """Deletes file from files ystem
    when corresponding `Sales` object is changed.
    """
    if not instance.pk:
        return False
    try:
        old_file = Sales.objects.get(pk=instance.pk).invoice
    except:
        return False
    if not old_file:
        return False
    new_file = instance.invoice
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class SalesItems(models.Model):
    fk_sales = models.ForeignKey(Sales, verbose_name = _('Sales'),related_name = _('Sales'))
    fk_import = models.ForeignKey(Imports, verbose_name = _('Import'),related_name = _('SoldImport'))
    quantity = models.IntegerField(default=0,validators = [MinValueValidator(0)], verbose_name=_('Quantity'))
    price = models.FloatField(default=0,validators = [MinValueValidator(0.0)] ,verbose_name=_('Price per Item'))

    def __unicode__(self):
        return unicode(self.fk_sales) +'-Q'+ unicode(self.quantity) +'-P'+ unicode(self.price)
    
    class Meta:
        verbose_name = _('Sales Item')
        verbose_name_plural = _('Sales Items')
    