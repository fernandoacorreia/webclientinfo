from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^info/(?P<url_id>\d+)/$', 'clientinfo.views.info'),
    url(r'^go/(?P<url_id>\d+)/$', 'clientinfo.views.go', name="url_go"),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
