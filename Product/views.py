from django.shortcuts import render
from Product.models import Transfers, Sales
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.db.models.aggregates import Sum


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







