from django.conf.urls import url
from Website import views

urlpatterns = (    
    url(r'^$',views.index),
    url(r'^products',views.products),
    url(r'^contact',views.contanct),
)
