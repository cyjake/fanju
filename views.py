from google.appengine.api import users
from google.appengine.ext import db

from common import redirect, respond
from models import Group, Fee, UserAlias

def home(request):
    fees = get_fees()
    params = { 'fees': fees, }
    
    return respond('home.html', params)

def page_redirect(request, url):
    params = {}
    for code in ('login', 'power', 'param', 'missing'):
        if request.GET.has_key(code):
            params.update({"code_%s" % code: True,})

    params.update({'url': "/%s" % url,})
    return respond('redirect.html', params)

def page_not_found(request):
    return respond('404.html')

def get_fees(group_id=None):
    """
    please notice, there's a different function in helpers.py
    with the same name.
    """
    fee_query = db.Query(Fee)
    if group_id:
        group = Group.get_by_id(group_id)
        fee_query.filter("group =", group)
    fee_query.order('-date')
    fees = fee_query.fetch(20)
    return fees
