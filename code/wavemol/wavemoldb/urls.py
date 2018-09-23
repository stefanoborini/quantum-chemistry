from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import os

urlpatterns = patterns('',
    # Example:

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),

    # Web access stuff
    # the resource lists
    (r'^runs/?$', 'wavemoldb.application.views.web.runs.render'),
    # specific resources
    (r'^resources/{(.*)}/?$', 'wavemoldb.application.views.web.resource.render' ),
    (r'^searchsnippets/{(.*)}/?$', 'wavemoldb.application.views.web.search.searchsnippets.render'),
    (r'^search/?$', 'wavemoldb.application.views.web.search.render'),
    (r'^/?$', 'wavemoldb.application.views.web.render'),


    (r'^js/plugins/(?P<plugin_name>.*)/(?P<file_name>.+\.js)$', 'wavemoldb.application.views.web.plugins.jsrender'),
    (r'^css/plugins/(?P<plugin_name>.*)/(?P<file_name>.+\.css)$', 'wavemoldb.application.views.web.plugins.cssrender'),
    (r'^java/plugins/(?P<plugin_name>.*)/(?P<file_name>.+\.jar)$', 'wavemoldb.application.views.web.plugins.javarender'),

    # API version 2.0. 
    (r'^api/v2/resources/{(.*)}/?$', 'wavemoldb.application.views.api.v2.resource.render'),
    (r'^api/v2/import/?$', 'wavemoldb.application.views.api.v2.import.dispatch'),

    # passthrough stuff
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.WEB_ACCESSIBLE_BASE_DIR,'css')}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.WEB_ACCESSIBLE_BASE_DIR,'images')}),
    (r'^applets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.WEB_ACCESSIBLE_BASE_DIR,'applets')}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.WEB_ACCESSIBLE_BASE_DIR,'js')}),
    (r'^cache/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.WEB_ACCESSIBLE_BASE_DIR,'cache')}),

    # everything else, return 404
    (r'^.*$', 'wavemoldb.application.views.web.notfound.render'),

)
