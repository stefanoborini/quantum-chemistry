# Django settings for project.

import os, os.path, sys
root = os.path.abspath( os.path.dirname( __file__ ) or os.curdir )
sys.path.insert( 0, os.path.normpath( root ) ) 
sys.path.insert( 0, os.path.normpath( os.path.join( root, 'deps', 'lib', 'python') ) ) 
sys.path.insert( 0, os.path.normpath( os.path.join( root, 'deps', 'lib', 'python2.5','site-packages') ) ) 

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Main database settings
DATABASE_ENGINE = 'mysql'               # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'developdb'             # Or path to database file if using sqlite3.
DATABASE_USER = 'developdb'             # Not used with sqlite3.
DATABASE_PASSWORD = 'developdb'         # Not used with sqlite3.
DATABASE_HOST = ''                      # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                      # Set to empty string for default. Not used with sqlite3.
DATABASE_OPTIONS = dict(charset="utf8")

# RDF database settings
RDF_DATABASE_NAME = 'developrdf'
RDFGRAPH_CONNECT = "host=localhost,password="+DATABASE_PASSWORD+",user="+DATABASE_USER+",db="+RDF_DATABASE_NAME
RDFGRAPH_URI = "urn:uuid:a19f9b78-cc43-4866-b9a1-4b009fe91f52"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '++!88p9mfl1a28@q(tq_b+^xc5(8*1l*xbsco6v0g62xyb1f^w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'wavemoldb.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(root, "templates"), os.path.join(root,"css"), 
    os.path.join(root, "application/views/web/plugins"), 
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'wavemoldb.application',
)

APPEND_SLASH=True

WEB_ACCESSIBLE_BASE_DIR = os.path.join(root,'web')

filestorage_settings = {}
filestorage_settings["WEB_CACHE_BASE_DIR"] = os.path.join(WEB_ACCESSIBLE_BASE_DIR, "cache")
filestorage_settings["WEB_CACHE_WEB_BASE_URL"] = "/cache/"
filestorage_settings["LOCAL_CACHE_BASE_DIR"] = os.path.join(root, "localcache")

VERSION="0.1.0"


# without trailing /!
HOST_BASE = "http://localhost:8000"
LOGDIR=os.path.join(root, "logs")
NAME="GRRM"

