from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib import databrowse
from Gammu.models import Inbox, Outbox, SentItems

databrowse.site.register(Inbox)
databrowse.site.register(Outbox)
databrowse.site.register(SentItems)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Uju.views.home', name='home'),
    # url(r'^uju/', include('uju.foo.urls')),
    url(r'^uju/server/', include('uju.UjuServer.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^gammu/(.*)', databrowse.site.root),
)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
