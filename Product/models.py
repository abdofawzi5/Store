from django.db import models
from django.utils.translation import  ugettext_lazy as _
from Company.models import Location
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator

SHORT_NAME_LENGTH = 20
LONG_NAME_LENGTH = 50
SHORT_TEXT_LENGTH = 100
LONG_TEXT_LENGTH = 800

class Category(models.Model):
    name = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name=_('Category'))

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Product(models.Model):
    name = models.CharField(max_length = SHORT_NAME_LENGTH, verbose_name=_('Product Name'))
    photo = models.ImageField(blank = True, null = True ,upload_to = 'Product/' ,verbose_name = _('photo'))
    description = models.CharField(blank = True, null = True,max_length = LONG_TEXT_LENGTH, verbose_name = _('Description'))
    price = models.FloatField(blank=True,null=True,default=0 ,verbose_name=_('Price'))
    fk_category = models.ForeignKey(Category, verbose_name=_('Category'))
    createdAt = models.DateField(auto_now_add=True , verbose_name = _('Created At'))

    def __unicode__(self):
        return unicode(self.fk_category) + ' - ' + unicode(self.name)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Imports(models.Model):
    fk_product = models.ForeignKey(Product, verbose_name = _('Product Product'),related_name = _('Product'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
    price = models.FloatField(blank=True,null=True,default=0 ,verbose_name=_('Total Price'))
    the_date = models.DateField(default=date.today ,blank=False, verbose_name = _('Date'))
    
    def __unicode__(self):
        return unicode(self.fk_product) +'('+ unicode(self.the_date)+')'
    
    class Meta:
        verbose_name = _('Import')
        verbose_name_plural = _('Imports')



class Transfers(models.Model):
    fk_import = models.ForeignKey(Imports, verbose_name = _('Imports'),related_name = _('Imports'))
    fk_location_from = models.ForeignKey(Location, null = True, verbose_name = _('Transfer From'),related_name = _('TransferFrom'))
    fk_location_to = models.ForeignKey(Location, verbose_name=_('Transfer To'),related_name = _('TransferTo'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
    price = models.FloatField(default=0 ,verbose_name=_('Price per Item')) 
    discount_rate = models.FloatField(default=0,validators = [MinValueValidator(0.0), MaxValueValidator(10.0)] ,verbose_name=_('Discount Rate'))
    the_date = models.DateField(default=date.today ,blank=False, verbose_name = _('Date'))
    
    def __unicode__(self):
        return unicode(self.fk_import) +'('+ unicode(self.the_date)+')'
    
    class Meta:
        verbose_name = _('Transfer')
        verbose_name_plural = _('Transfers')

class Sales(models.Model):
    fk_transfer = models.ForeignKey(Transfers, verbose_name = _('Transfers'),related_name = _('Transfers'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))
    price = models.FloatField(default=0 ,verbose_name=_('Price per Item'))
    bill = models.ImageField(blank = True, null = True ,upload_to = 'bill/' ,verbose_name = _('bill'))
    the_date = models.DateField(default=date.today ,blank=False, verbose_name = _('Date'))
    
    def __unicode__(self):
        return unicode(self.fk_transfer.fk_import) +'('+ unicode(self.the_date)+')'
    
    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')


    