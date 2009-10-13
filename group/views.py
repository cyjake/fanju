# -*- coding: utf-8 -*-
import cgi
import sys

from google.appengine.api import users
from google.appengine.ext import db
from django.http import Http404

from common import redirect, respond, post_param, get_param
from models import Group, UserAlias, Fee
from helpers import get_group, save_users, get_fees, get_users, check_user, get_user

def home(request):
    group_query = db.Query(Group)
    groups = group_query.fetch(20)
    if len(groups) <1:
        return redirect("/group/edit/")

    return respond('group_home.html', {'groups': groups,})

def detail(request, group_id):
    group = get_group(group_id)
    if not group:
        raise Http404()
        
    require_privilege = check_user(group)
        
    summaries = [] +group.summaries
    summaries.sort()
    due_payer_index = group.summaries.index(summaries[0])
    due_payer = get_user(group.members[due_payer_index])

    params = {'fees': get_fees(group),
              'members': get_users(group),
              'is_valid_user': not require_privilege,
              'group': group,
              'due_payer': due_payer.name,
              'due_amount': -summaries[0], }

    return respond('group_detail.html', params)
    
def edit(request, group_id):
    param = {}
    if group_id:
        group = get_group(group_id)
        require = check_user(group)
        if require:
            return redirect("/redirect/?%s" % require)
        
        users = get_users(group)
        param.update({'group': group,
                      'users': users,})

    errs = get_param(request, 'errs')
    if errs:
        errs = errs.split(',')
        for err in errs:
            param.update({"%s_error" % err: True,})
    return respond('group_edit.html', param)

def delete(request, group_id):
    try:
        group = get_group(group_id)
        require = check_user(group)
        if require:
            raise Exception("invalid user")
        if not request.GET.has_key('confirm'):
            params = {'name': group.name,
                      'confirm': "%s?confirm" % request.path,
                      'cancel': "/group/%s" % group_id,}
            return respond("confirm.html", params)
    except ValueError:
        return redirect('/redirect/?param')
    except:
        return redirect("/redirect/?%s" % require)
    else:
        for member_id in group.members:
           member = get_user(member_id)
           member.delete()
        group.delete()
        return home(request)

def save(request):
    password = post_param(request, 'password')
    name = post_param(request, 'name')
    members = post_param(request, 'members').split()
    group_id = post_param(request, 'group_id')
    owner_email = post_param(request, 'owner')
    group = None
    if group_id:
        try:
            group = get_group(long(group_id))
            require = check_user(group)
            if require:
                return redirect("/redirect/?%s" % require)
        except:
            return redirect('/group/edit/?errs=group_id')

        for member in get_users(group):
            if member.name not in members:
                return redirect('/group/edit/%s?errs=members' % group.key().id())

    members = save_users(members, group)
    owner = None
    try:
        owner = users.User(owner_email)
    except:
        owner = users.get_current_user()
        
    if group:
        group.members = members
        group.owner = owner
    else:
        group = Group(members = members,
                      password = password,
                      name = name,
                      owner = owner)

    while len(group.summaries) < len(members):
        group.summaries.append(0.0)
            
    group.put()
    return redirect('/redirect/group/')
