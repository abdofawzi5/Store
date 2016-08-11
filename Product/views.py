from Product.models import Transfers, SalesItems, Imports
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
    return importsAvaliable




