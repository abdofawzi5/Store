from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from Store import settings,views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Store.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),

    # to protect require login in media
    url(r'^media/(?P<filename>.*)$', views.protected_media),
] 

# if settings.DEBUG is True:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
