# -*- coding: utf-8 -*-
import cgi

from google.appengine.api import users
from google.appengine.ext import db
from datetime import datetime

from common import redirect, respond, post_param, post_params
from models import Group, UserAlias, Fee
from helpers import get_group, get_user, get_fee, get_users, check_user

def delete(request, fee_id):
    try:
        fee = get_fee(fee_id)
        group_id = fee.group.key().id()
        if not request.GET.has_key('confirm'):
            params = {'name': u"%s的%d个家伙腐败掉%.1f的证据" % (fee.group.name, len(fee.participants), fee.amount),
                      'confirm': "%s?confirm" % request.path,
                      'cancel': "/group/%s" % group_id,}
            return respond("confirm.html", params)

        require = check_user(fee.group)
        if require:
            return redirect("/redirect/?%s" % require)

        update_group_summary(fee, add_fee=False)
        fee.delete()
    except:
        raise
    else:
        return redirect("/redirect/group/%s" % group_id)

def save(request):
    try:
        group_id = long(post_param(request, 'group_id'))
        group = get_group(group_id)
        require = check_user(group)
        if require: 
            return redirect("/redirect/?%s" % require)
            
        amount = float(post_param(request, 'amount'))
        if amount <0:
            raise ValueError('amount can not be negative')
        
        payer_id = long(post_param(request, 'payer'))
        participants = map(lambda x: long(x), post_params(request, 'participants'))
        if len(participants) <1:
            raise ValueError('a meal with no attendee?')
        if payer_id not in participants:
            raise ValueError('...I have nothing to say.')
        date = None
        date_str = post_param(request, 'date')
        if date_str:
            date = datetime.strptime(date_str, "%Y/%m/%d")
    except:
        return redirect('/redirect/group/%s?%s' % (group_id, 'param'))
    else:
        save_fee(group, amount, payer_id, participants, date)
        return redirect('/redirect/group/%s' % group_id)

def save_fee(group, amount, payer_id, participants, date):
    fee = add_fee(group, amount, payer_id, participants, date)
    update_group_summary(fee, add_fee=True)

def add_fee(group, amount, payer_id, participants, date=None):
    fee = Fee(amount = amount,
              payer = get_user(payer_id),
              participants = participants,
              group = group,)
    if date:
        fee.date = date
    fee.put()
    return fee

def update_group_summary(fee, add_fee=True):
    group, payer_id = fee.group, fee.payer.key().id()
    average = fee.amount / len(fee.participants)
    for p in range(len(group.members)):
        if group.members[p] == payer_id:
            if add_fee:
                group.summaries[p] += fee.amount -average
            else:
                group.summaries[p] -= (fee.amount -average)
        elif group.members[p] in fee.participants:
            if add_fee:
                group.summaries[p] -= average
            else:
                group.summaries[p] += average
                
    group.put()
