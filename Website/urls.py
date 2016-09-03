from django.conf.urls import url
from Website import views

urlpatterns = (    
    url(r'^$',views.index),
    #url(r'^index$',views.view),
)
