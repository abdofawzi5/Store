from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.translation import  ugettext_lazy as _
from datetime import date, timedelta, datetime
from Company.views import getAllLocations,getLocation
from Product.views import productAndCategorySoldQuantity, companyAvailableQuantity,locationAvailableQuantity
from Charts.views import drawChartWithDrilldown

@login_required(login_url='/admin/login/')
def companyLevel(request):
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
    context['companyAvailableQuantity'] = companyAvailableQuantity()
    return context

@login_required(login_url='/admin/login/')
def locationLevel(request):
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
    context['locationAvailableQuantity'] = locationAvailableQuantity(context['location'].id)
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









