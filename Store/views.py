from django.contrib.auth.decorators import login_required
from Store import settings
from django.shortcuts import redirect
from django.shortcuts import render

from django.views.static import serve

# @login_required(login_url='/admin/login/')
def protected_media(request, filename=None, show_indexes=False):
    foldersName = ['Advertisement','company_logo','Product']
    for folderName in foldersName:
        if folderName in filename:
            return serve(request, filename,settings.MEDIA_ROOT,  show_indexes)
    if request.user.is_authenticated():
        return serve(request, filename,settings.MEDIA_ROOT,  show_indexes)
    return redirect('/admin/login/')
