from google.appengine.ext import db

class UserAlias(db.Model):
    """ westpark members are not all google registerd uers.    
    """
    google_id = db.UserProperty()
    name = db.StringProperty(required=True)
    
class Group(db.Model):
    members = db.ListProperty(long, required=True)
    name = db.StringProperty(required=True)
    summaries = db.ListProperty(float)
    owner = db.UserProperty()

class Fee(db.Model):
    payer = db.ReferenceProperty(UserAlias)
    participants = db.ListProperty(long, required=True)
    group = db.ReferenceProperty(Group)
    amount = db.FloatProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)


