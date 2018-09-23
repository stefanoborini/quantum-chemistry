import os, sys
runtime_dir = "/home/db/runtimes/wavemol-py25"
apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path.append( os.path.join(runtime_dir, "lib", "python2.5", "site-packages"))
os.environ["DJANGO_SETTINGS_MODULE"] = "wavemoldb.settings"
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
