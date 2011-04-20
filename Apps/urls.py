from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^genConfig/', include('genConfig.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^show_app_form/$','Apps.GenApp.views.show_app_form'),
    (r'^ajax_gen_app/$','Apps.GenApp.views.ajax_gen_app'),
    (r'^show_op_form/$','Apps.GenForm.views.show_op_form'),
    (r'^gen_op_form/$','Apps.GenForm.views.gen_op_form'),
)
