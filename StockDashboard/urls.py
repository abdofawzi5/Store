from django.conf.urls import url
from StockDashboard import views

urlpatterns = (    
    url(r'^$',views.companyLevel),
    url(r'^location$',views.locationLevel),
    url(r'^imports$',views.importsDetails),
    #url(r'^index$',views.view),
)
