from django.conf.urls.defaults import *

urlpatterns = patterns(
    'fee',
    (r'^save/$', 'views.save'),
    (r'^delete/(\d+)$', 'views.delete'),
    )
