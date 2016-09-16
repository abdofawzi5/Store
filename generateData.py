import django
import os
# from Store import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Store.settings'
django.setup()

from Company.models import Company, LocationType, Location
from Product.models import Product, ProductCategory, Imports, Transfers, Sales,\
    SalesItems
from datetime import timedelta, date
import random

productsIDs = []
locationsIDs = []
# company = Company(name='stocky',slogan='MySlogan',short_description='Stocky is an stock management system',long_description='Stocky is an stock management system, can Monitor Data, Measure sales performance and generate invoices',phone='0xxxxxxxxxx',address='3x street, City, Country ',email='name@domain.com')
# company.save()
# print "Done adding Company"

locationsList = ['Store','Stock']
for locationName in locationsList:
    locationType = LocationType(type=locationName)
    locationType.save()
    for i in range(1,3):
        location = Location(fk_locationType=locationType,name=locationName+str(i),phone='0xxxxxxxxx',address=str(locationName+str(i))+' street, City, Country',email=str(locationName+str(i))+'@domain.com')
        location.save()
        locationsIDs.append(location)
print "Done adding Location"


productCategory = ProductCategory(name='TV')
productCategory.save()
products = ['Samsung UA40J5200AK','LG 49LH590V','Samsung UA40J5000','LG 42LF550T']
for productName in products:
    product = Product(fk_category=productCategory,name=productName)
    product.save()
    productsIDs.append(product)
     
productCategory = ProductCategory(name='Laptop')
productCategory.save()
products = ['Apple Pro','Dell N5110','Lenovo z5170','ASUS Transformer']
for productName in products:
    product = Product(fk_category=productCategory,name=productName)
    product.save()
    productsIDs.append(product)
 
productCategory = ProductCategory(name='Mobiles')
products = ['iPhone','sony z5','Samsung Note 6','ASUS Zenfone selfie']
productCategory.save()
for productName in products:
    product = Product(fk_category=productCategory,name=productName)
    product.save()
    productsIDs.append(product)
print "Done adding Products"

startDate = date.today() - timedelta(350)
endDate = date.today() - timedelta(10)
while startDate < endDate:
    if random.randint(1, 3) == 1:
        quantity = random.randint(20, 50)
        oneItemPrice = random.randint(3000, 5000)
        price = quantity * oneItemPrice
        imports = Imports(fk_product=random.choice(productsIDs),quantity=quantity,price = price,selling_price=oneItemPrice+random.randint(500, 1000),the_date=startDate)
        imports.save()
        while quantity > 0:
            transDate = startDate + timedelta(random.randint(1,7))
            oneLocation = random.choice(locationsIDs)
            transQuantity = random.randint(1,quantity)
            quantity -= transQuantity
            trans = Transfers(fk_import=imports,fk_location_to=oneLocation,quantity=transQuantity,the_date=transDate)
            trans.save()
            while transQuantity > 0:
                soldDate = transDate + timedelta(random.randint(1,7))
                soldQuantity = random.randint(1,transQuantity)
                transQuantity -= soldQuantity
                sales = Sales(fk_location=oneLocation,the_date=soldDate,name='ClientName',phone='0xxxxxxxxx')
                sales.save()
                salesItems = SalesItems(fk_sales=sales,fk_import=imports,quantity=soldQuantity,price=imports.selling_price)
                salesItems.save()
    else:
        startDate += timedelta(1)
print "Done adding imports and sales"

print "Done"














