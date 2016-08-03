from django.contrib.auth.decorators import login_required
import os
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

@login_required
def protected_media(request, filename):
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response