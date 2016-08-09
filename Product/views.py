from django.shortcuts import render
from Product.models import Transfers, Sales
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.db.models.aggregates import Sum
from django.db.models.expressions import Case, When
from django.db.models.fields import IntegerField


def availableQuantityInLocation(fk_import_obj,fk_location_obj):
    availableQuantity = 0
    totalTransferred = Transfers.objects.filter(Q(fk_location_from = fk_location_obj)|Q(fk_location_to = fk_location_obj),fk_import=fk_import_obj)
    for oneTransfer in totalTransferred:
        if oneTransfer.fk_location_from == fk_location_obj:
            availableQuantity -= oneTransfer.quantity
        if oneTransfer.fk_location_to == fk_location_obj:
            availableQuantity += oneTransfer.quantity
    soldQuantity = Sales.objects.filter(fk_import = fk_import_obj, fk_location = fk_location_obj).aggregate(soldQuantity = Coalesce(Sum('quantity'),0))['soldQuantity']
    availableQuantity -= soldQuantity
    return availableQuantity

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





