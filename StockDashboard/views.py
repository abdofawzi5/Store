from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.utils.translation import  ugettext_lazy as _
from datetime import date, timedelta, datetime
from Company.models import Location
from Product.models import Imports
from Company.views import getAllLocations,getLocation
from Product.views import productAndCategorySoldQuantity, companyAvailableQuantity,locationAvailableQuantity,availableImports,importsDetailByIDs,getSalesPerDay
from Charts.views import drawChartWithDrilldown, drawChart, xAxisListDates

@login_required(login_url='/admin/login/')
def companyLevel(request):
    context = companyLevelContext(request)
    return render(request,'StockDashboard/companyLevel.html',context)

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
    
    context['salesPerDayChart'] = salesPerDayChart(unicode(_('Company Income')+""),Location.objects.all(), dateFilter-timedelta(30), dateFilter)

    return context

@login_required(login_url='/admin/login/')
def locationLevel(request):
    context = locationLevelContext(request)
    return render(request,'StockDashboard/locationLevel.html',context)

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
    context['salesPerDayChart'] = salesPerDayChart(unicode(context['location'].name)+'-'+unicode(_('Income')+""),[context['location']], dateFilter-timedelta(30), dateFilter)
    return context

@login_required(login_url='/admin/login/')
def importsDetails(request):
    context = importsDetailsContext(request)
    return render(request,'StockDashboard/importsDetails.html',context)

def importsDetailsContext(request):
    context = {}
    dateFilter = request.GET.get('dateFilter')
    if dateFilter is None:
        dateFilter = date.today()
    else:
        dateFilter = datetime.strptime(dateFilter, '%Y-%m-%d').date()
    context['dateFilter'] = str(dateFilter)
    context['locations'] = getAllLocations()
    locations = Location.objects.all()
    availableImportsIDs = availableImports(locations,dateFilter)
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
        dic['name'] = unicode(oneQuantity['category_name'])
        categoryQuantity = 0
        dic['data'] = []
        for product in oneQuantity['products']:
            dic['data'].append([unicode(product['product_name']),product['quantity']])
            categoryQuantity += product['quantity']
        dic['value'] = categoryQuantity
        dataDictionaryInList.append(dic)
    return drawChartWithDrilldown(dataDictionaryInList,chartTitle,None, None, None, None, None)

def salesPerDayChart(chartTitle,locations,fromDate,toDate):
    dataDictionaryInList = []
    salesPerDay = getSalesPerDay(locations, fromDate, toDate)
    dataDictionaryInList.append({'data':salesPerDay,'name':_('Company Income')+""})
    if len(locations) > 1:
        for oneLocation in locations:
            salesPerDay = getSalesPerDay([oneLocation], fromDate, toDate)
            dataDictionaryInList.append({'data':salesPerDay,'name':unicode(oneLocation.name)+'-'+unicode(_('Income'))})
    else:
        for salesPerDay in dataDictionaryInList:
            salesPerDay['name'] =  chartTitle
            break;
    return drawChart(dataDictionaryInList, chartTitle, None, None, None, '$', xAxisListDates(fromDate,toDate))

