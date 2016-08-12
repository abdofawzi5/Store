from django.conf.urls import url
from StockDashboard import views

urlpatterns = (    
    url(r'^$',views.companyLevel),
    #url(r'^index$',views.all_farms),
)
