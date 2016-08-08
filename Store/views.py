from django.contrib.auth.decorators import login_required
import os
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from Store import settings

from django.views.static import serve
#from django.core.servers.basehttp import FileWrapper

@login_required
def protected_media(request, filename=None, show_indexes=False):
    return serve(request, filename,settings.MEDIA_ROOT,  show_indexes)

