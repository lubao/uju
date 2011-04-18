from django.conf.urls.defaults import patterns, include, url
import settings
# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'UjuServer.views.home', name='home'),
)
