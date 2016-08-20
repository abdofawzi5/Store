from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta, datetime
from Company.views import getAllLocations
from Product.views import productAndCategoryQuantity
from Charts.views import drawChart, xAxisListDates, drawChartWithDrilldown

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
    context['productQuantitySummeryChart'] = productQuantitySummeryChart(dateFilter)
    return context

def productQuantitySummeryChart(dateFilter):
    totalQuantity = productAndCategoryQuantity(dateFilter - timedelta(30), dateFilter)
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
    print dataDictionaryInList
    return drawChartWithDrilldown(dataDictionaryInList, 'Sales Quantity last 30 days',None, None, None, None, None)









