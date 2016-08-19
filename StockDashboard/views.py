from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import date
from Company.views import getAllLocations

@login_required(login_url='/admin/login/')
def companyLevel(request):
    context = companyLevelContext(request)
    return render_to_response('StockDashboard/companyLevel.html',context)

def companyLevelContext(request):
    context = {}
    dateFilter = request.GET.get('dateFilter')
    if dateFilter is None:
        dateFilter = date.today()
    context['dateFilter'] = str(dateFilter)
    context['locations'] = getAllLocations()  
    return context










