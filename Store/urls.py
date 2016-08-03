from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from Store import settings,views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Store.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    # to protect require login in media
    url(r'^media/(?P<filename>.*)$', views.protected_media),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)