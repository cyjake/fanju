from models import Group, UserAlias, Fee
from google.appengine.ext import db
from google.appengine.api import users

def get_group(id):
    try:
        return Group.get_by_id(int(id))
    except:
        return None

def save_users(names, group=None):
    members, users = [], []
    if group:
        members = group.members
        users = get_users(group)
    for name in names:
        for user in users:
            if name == user.name:
                break
        else:
            user = UserAlias(name=name)
            user.put()
            members.append(user.key().id())

    return members

def get_fees(group):
    query = Fee.gql("WHERE group = :1 ORDER BY date DESC", group)
    raws = query.fetch(20)
    fees = []
    for raw in raws:
        fee = {}
        fee['date'] = raw.date
        fee['id'] = raw.key().id()
        fee['spenders'] = []
        average = raw.amount / len(raw.participants)
        for m in group.members:
            if m == raw.payer.key().id():
                spender = {'amount': raw.amount -average,
                           'payer': True,}
            elif m in raw.participants:
                spender = {'amount': -average,}
            else:
                spender = {'amount': 0,}
            fee['spenders'].append(spender)
        fees.append(fee)
    return fees

def get_users(group):
    users = []
    for member_id in group.members:
        users.append(UserAlias.get_by_id(member_id))
    return users

def get_fee(id):
    try:
        return Fee.get_by_id(long(id))
    except:
        return None

def get_user(id):
    try:
        return UserAlias.get_by_id(long(id))
    except:
        return None

def check_user(group=None):
    user = users.get_current_user()
    if not user:
        return 'login'

    if group and user != group.owner:
        for member in get_users(group):
            if user == member.google_id:
                break
        else:
            return 'power'
