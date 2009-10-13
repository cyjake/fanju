# common functions
import os
from django import shortcuts
from django.http import HttpResponseRedirect
from google.appengine.api import users

def post_param(request, key):
    if request.POST.has_key(key):
        return unicode(request.POST[key], 'utf-8')

def post_params(request, key):
    if request.POST.has_key(key):
        return request.POST.getlist(key)

def get_param(request, key):
    if request.GET.has_key(key):
        return unicode(request.GET[key], 'utf-8')

def redirect(to):
    redirect_class = HttpResponseRedirect
    return redirect_class(to)
    
def respond(file, params=None):
    if params is None:
        params = {}
    user = users.get_current_user()
    if user:
        params['user'] = user
        params['sign_out'] = users.CreateLogoutURL('/')
        params['is_admin'] = (users.IsCurrentUserAdmin() and
                              'Dev' in os.getenv('SERVER_SOFTWARE'))
    else:
        params['sign_in'] = users.CreateLoginURL('/')
    template = os.path.join(os.path.dirname(__file__), 'templates', file)
    return shortcuts.render_to_response(template, params)

