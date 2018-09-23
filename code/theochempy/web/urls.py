from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
import os

def rootDir():
    return os.path.dirname(__file__)


urlpatterns = patterns('',
    # Example:
    # (r'^costmap/', include('costmap.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
    (r'^browsedb/(.*)/(.*)', "costmap.application.views.browsemol"),
    (r'^browsedb/(.*)', "costmap.application.views.browsedb"),
    (r'^json/searchdb/$', 'costmap.application.views.json.searchdb'),
    (r'^search/', "costmap.application.views.search"),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(rootDir(),'css')}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(rootDir(),'images')}),
    (r'^applets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(rootDir(),'applets')}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(rootDir(),'js')}),
    (r'^cache/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(rootDir(),'cache')}),
    (r'.*', 'costmap.application.views.index'),
)
