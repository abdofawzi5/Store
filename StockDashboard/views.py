from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.translation import  ugettext_lazy as _
from django.utils.translation import activate
from datetime import date, timedelta, datetime
from Company.models import Location
from Product.models import Imports
from Company.views import getAllLocations,getLocation
from Product.views import productAndCategorySoldQuantity, companyAvailableQuantity,locationAvailableQuantity,availableImports,importsDetailByIDs
from Charts.views import drawChartWithDrilldown

@login_required(login_url='/admin/login/')
def companyLevel(request):
    activate('en')
    context = companyLevelContext(request)
    return render_to_response('StockDashboard/companyLevel.html',context)

def companyLevelContext(request):
    context = {}
    dateFilter = request.GET.get('dateFilter')
    if dateFilter is None:
        dateFilter = date.today()
    else:
        dateFilter = datetime.strptime(dateFilter, '%Y-%m-%d').date()
    context['dateFilter'] = str(dateFilter)
    context['locations'] = getAllLocations()
    fromDate = dateFilter.replace(day=1)
    toDate = dateFilter
    title = unicode(_("Sold Quantity in "))+str(fromDate.strftime("%B"))+' ' + str(fromDate.strftime("%Y"))
    context['soldQuantityThisMonthChart'] = soldQuantityChart(title,fromDate, toDate,None)
    fromDate = (dateFilter-timedelta(60)).replace(day=1)
    try:
        toDate = (dateFilter-timedelta(60)).replace(day=31)
    except:
        toDate = (dateFilter-timedelta(60)).replace(day=30)
    title = unicode(_("Sold Quantity in "))+str(fromDate.strftime("%B"))+' ' + str(fromDate.strftime("%Y"))
    context['soldQuantityLastMonthChart'] = soldQuantityChart(title,fromDate, toDate,None)
    context['companyAvailableQuantity'] = companyAvailableQuantity(dateFilter)
    return context

@login_required(login_url='/admin/login/')
def locationLevel(request):
    activate('en')
    context = locationLevelContext(request)
    return render_to_response('StockDashboard/locationLevel.html',context)

def locationLevelContext(request):
    context = {}
    dateFilter = request.GET.get('dateFilter')
    if dateFilter is None:
        dateFilter = date.today()
    else:
        dateFilter = datetime.strptime(dateFilter, '%Y-%m-%d').date()
    context['dateFilter'] = str(dateFilter)
    context['locations'] = getAllLocations()
    context['location'] = getLocation(int(request.GET.get('id')))
    fromDate = dateFilter.replace(day=1)
    toDate = dateFilter
    title = unicode(_("Sold Quantity in "))+str(fromDate.strftime("%B"))+' ' + str(fromDate.strftime("%Y"))
    context['soldQuantityThisMonthChart'] = soldQuantityChart(title,fromDate, toDate,[context['location'].id])
    fromDate = (dateFilter-timedelta(60)).replace(day=1)
    try:
        toDate = (dateFilter-timedelta(60)).replace(day=31)
    except:
        toDate = (dateFilter-timedelta(60)).replace(day=30)
    title = unicode(_("Sold Quantity in "))+str(fromDate.strftime("%B"))+' ' + str(fromDate.strftime("%Y"))
    context['soldQuantityLastMonthChart'] = soldQuantityChart(title,fromDate, toDate,[context['location'].id])
    context['locationAvailableQuantity'] = locationAvailableQuantity(context['location'].id,dateFilter)
    return context

@login_required(login_url='/admin/login/')
def importsDetails(request):
    activate('en')
    context = importsDetailsContext(request)
    return render_to_response('StockDashboard/importsDetails.html',context)

def importsDetailsContext(request):
    context = {}
    dateFilter = request.GET.get('dateFilter')
    if dateFilter is None:
        dateFilter = date.today()
    else:
        dateFilter = datetime.strptime(dateFilter, '%Y-%m-%d').date()
    context['dateFilter'] = str(dateFilter)
    context['locations'] = getAllLocations()
    availableImportsIDs = availableImports(Location.objects.all())
    context['availableImports'] = importsDetailByIDs(availableImportsIDs,dateFilter)
    fromDate = (dateFilter-timedelta(90)).replace(day=1)
    last3monthImports =  Imports.objects.filter(the_date__gte = fromDate,the_date__lte=dateFilter).values('id')
    last3monthImportsList = []
    for oneImport in last3monthImports:
        if oneImport['id'] not in availableImportsIDs:
            last3monthImportsList.append(oneImport['id'])

    context['last3monthImports'] = importsDetailByIDs(last3monthImportsList,dateFilter)
    
    return context

"""
********************************************************************************
********************************* Build Charts *********************************
********************************************************************************
"""

def soldQuantityChart(chartTitle,fromDate,toDate,locationsIDs):
    totalQuantity = productAndCategorySoldQuantity(fromDate,toDate,locationsIDs)
    dataDictionaryInList = []
    for oneQuantity in totalQuantity:
        dic = {}
        dic['name'] = str(oneQuantity['category_name'])
        categoryQuantity = 0
        dic['data'] = []
        for product in oneQuantity['products']:
            dic['data'].append([str(product['product_name']),product['quantity']])
            categoryQuantity += product['quantity']
        dic['value'] = categoryQuantity
        dataDictionaryInList.append(dic)
    return drawChartWithDrilldown(dataDictionaryInList,chartTitle,None, None, None, None, None)





