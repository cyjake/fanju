from django.conf.urls.defaults import *

urlpatterns = patterns(
    'group',
    (r'^$', 'views.home'),
    (r'^(\d+)', 'views.detail'),
    (r'^edit/(\d*)$', 'views.edit'),
    (r'^save/$', 'views.save'),
    (r'^delete/(\d+)$', 'views.delete'),
    )
