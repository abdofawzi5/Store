from Product.models import Transfers, SalesItems, Imports, Sales
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.db.models.aggregates import Sum
from django.db.models.expressions import Case, When
from django.db.models.fields import IntegerField
from django.core.files import File
from Store import settings
import openpyxl

def generateBill(sales):
    path = settings.MEDIA_ROOT+'bills/temp/'
    filename = 'bill'+'-'+str(sales.id)+'-'+str(sales.id)+str(sales.the_date.year)+str(sales.the_date.month)+str(sales.the_date.day)+'.xls'
    wb = openpyxl.load_workbook(settings.MEDIA_ROOT+'bills/base/baseBill.xlsx')
    sheet = wb.get_sheet_by_name('bill')
    sheet['A1'].value = 'AAAAAAAAAAAAAAAAAAA'
    wb.save(path+filename)
    reopen = open(path+filename, "rb")
    django_file = File(reopen)
    return django_file
    

def availableQuantityInLocation(fk_import_obj,fk_location_obj):
    availableQuantity = 0
    totalTransferred = Transfers.objects.filter(Q(fk_location_from = fk_location_obj)|Q(fk_location_to = fk_location_obj),fk_import=fk_import_obj).aggregate(inTransfers = Coalesce(Sum(Case(When(fk_location_to = fk_location_obj, then='quantity'),output_field=IntegerField())),0) ,outTransfers = Coalesce(Sum(Case(When(fk_location_from = fk_location_obj, then='quantity'),output_field=IntegerField())),0))
    availableQuantity += totalTransferred['inTransfers']
    availableQuantity -= totalTransferred['outTransfers']
    soldQuantity = SalesItems.objects.filter(fk_import = fk_import_obj, fk_sales__fk_location = fk_location_obj).aggregate(soldQuantity = Coalesce(Sum('quantity'),0))['soldQuantity']
    availableQuantity -= soldQuantity
    return availableQuantity

def availableImports(locations):
    # show imports that has quantity
    all_imports = Imports.objects.all()
    importsAvaliable = []
    for one_import in all_imports:
        for one_location in locations:
            if availableQuantityInLocation(one_import, one_location) > 0:
                importsAvaliable.append(one_import.id)
                break
    return importsAvaliable

def availableImportsIDs(oneLocation):
    totalImports = Transfers.objects.filter(Q(fk_location_from = oneLocation)|Q(fk_location_to = oneLocation)).values('fk_import').annotate(inTransfers = Coalesce(Sum(Case(When(fk_location_to = oneLocation, then='quantity'),output_field=IntegerField())),0) ,outTransfers = Coalesce(Sum(Case(When(fk_location_from = oneLocation, then='quantity'),output_field=IntegerField())),0))
    totalSales = Sales.objects.filter(fk_location = oneLocation).values('fk_import').annotate(sold = Coalesce(Sum('quantity'),0))
    importsIDs = []
    for oneImport in totalImports:
        sold = 0
        try:
            sold =  (item for item in totalSales if item["fk_import"] == oneImport['fk_import']).next() ['sold']
        except:
            sold = 0
        availableQuantity = oneImport['inTransfers'] - oneImport['outTransfers'] - sold
        if availableQuantity > 0:
            importsIDs.append(oneImport['fk_import'])
    return importsIDs

def productAndCategorySoldQuantity(fromDate,toDate,locationsIDs):
    soldQuantity = SalesItems.objects.filter(fk_sales__the_date__gte = fromDate,fk_sales__the_date__lte = toDate)
    if locationsIDs is not None and len(locationsIDs) > 0:
        soldQuantity = soldQuantity.filter(fk_sales__fk_location__id__in = locationsIDs)
    soldQuantity = soldQuantity.values('fk_import__fk_product__fk_category__name','fk_import__fk_product__name').annotate(qunatity = Coalesce(Sum('quantity'),0))
    quantityList = []
    for sales in soldQuantity:
        found = next((item for item in quantityList if item["category_name"] == sales['fk_import__fk_product__fk_category__name']),False)
        if found == False:
            dict = {}
            dict['category_name'] = sales['fk_import__fk_product__fk_category__name']
            dict['products'] = [{'product_name':sales['fk_import__fk_product__name'],'quantity':sales['qunatity']}]
            quantityList.append(dict)
        else:
            found['products'].append({'product_name':sales['fk_import__fk_product__name'],'quantity':sales['qunatity']})
    return quantityList

def companyAvailableQuantity(dateFilter):
    productImports = Imports.objects.filter(the_date__lte = dateFilter).values('fk_product__name','fk_product__fk_category__name').annotate(inQuantity = Coalesce(Sum('quantity'),0))
    totalSales = SalesItems.objects.filter(fk_sales__the_date__lte = dateFilter).values('fk_import__fk_product__name','fk_import__fk_product__fk_category__name').annotate(sold = Coalesce(Sum('quantity'),0))
    productCategory = []
    for oneImport in productImports:
        found = next((item for item in productCategory if item["category_name"] == oneImport['fk_product__fk_category__name']),False)
        if found == False:
            dict = {}
            dict['category_name'] = oneImport['fk_product__fk_category__name']
            productDic = {'product_name':oneImport['fk_product__name'],'quantity':oneImport['inQuantity']}
            dict['products'] = [productDic]
            for sales in totalSales:
                if sales['fk_import__fk_product__name'] == productDic['product_name']:
                    productDic['quantity'] -= sales['sold']          
            productCategory.append(dict)
        else:
            productDic = {'product_name':oneImport['fk_product__name'],'quantity':oneImport['inQuantity']}
            for sales in totalSales:
                if sales['fk_import__fk_product__name'] == productDic['product_name']:
                    productDic['quantity'] -= sales['sold']                      
            found['products'].append(productDic)
    return productCategory
            
def locationAvailableQuantity(locationID,dateFilter):
    totaltransfers = Transfers.objects.filter(Q(fk_location_from__id = locationID)|Q(fk_location_to__id = locationID),the_date__lte = dateFilter).values('fk_import__fk_product__name','fk_import__fk_product__fk_category__name').annotate(inTransfers = Coalesce(Sum(Case(When(fk_location_to__id = locationID, then='quantity'),output_field=IntegerField())),0) ,outTransfers = Coalesce(Sum(Case(When(fk_location_from__id = locationID, then='quantity'),output_field=IntegerField())),0))
    totalSales = SalesItems.objects.filter(fk_sales__fk_location = locationID,fk_sales__the_date__lte = dateFilter).values('fk_import__fk_product__name','fk_import__fk_product__fk_category__name').annotate(sold = Coalesce(Sum('quantity'),0))

    productCategory = []
    for transfer in totaltransfers:
        found = next((item for item in productCategory if item["category_name"] == transfer['fk_import__fk_product__fk_category__name']),False)
        if found == False:
            dict = {}
            dict['category_name'] = transfer['fk_import__fk_product__fk_category__name']
            productDic = {'product_name':transfer['fk_import__fk_product__name'],'quantity':transfer['inTransfers']-transfer['outTransfers']}
            dict['products'] = [productDic]
            for sales in totalSales:
                if sales['fk_import__fk_product__name'] == productDic['product_name']:
                    productDic['quantity'] -= sales['sold']
            productCategory.append(dict)
        else:
            productDic = {'product_name':transfer['fk_import__fk_product__name'],'quantity':transfer['inTransfers']-transfer['outTransfers']}
            for sales in totalSales:
                if sales['fk_import__fk_product__name'] == productDic['product_name']:
                    productDic['quantity'] -= sales['sold']            
            found['products'].append(productDic)
    return productCategory
            
        
        
        
        
        
        