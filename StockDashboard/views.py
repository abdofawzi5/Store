from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login/')
def companyLevel(request):
    context = {}
    return render_to_response('StockDashboard/companyLevel.html',context)












