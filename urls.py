from django.conf.urls.defaults import *

handler404 = 'views.page_not_found'

urlpatterns = patterns(
    '',
    (r'^$', 'views.home'),
    (r'^group/', include('group.urls')),
    (r'^redirect/(.*)', 'views.page_redirect'),
    (r'^fee/', include('fee.urls')),
    )
