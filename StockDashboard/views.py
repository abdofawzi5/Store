from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required(login_url='/admin/login/')
def companyLevel(request):
    context = {}
    dateFilter = request.GET.get('dateFilter')
    print dateFilter
    if dateFilter is None:
        dateFilter = date.today()
    print dateFilter
    return render_to_response('StockDashboard/companyLevel.html',context)












