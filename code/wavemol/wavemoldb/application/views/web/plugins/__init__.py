from django import template
from django.template import loader
from django import http

import sys
import os
import inspect

class AbstractPlugin(object):
    def __init__(self):
        pass
    def name(self):
        raise NotImplementedError("name")
    def visibleName(self):
        # default implementation
        return self.name()
    def basePath(self):
        return os.path.join( os.path.dirname(os.path.abspath(__file__)), self.name())
    def templateBasePath(self):
        return os.path.join(self.name(),"files","templates") 
    def cssPath(self):
        path = self.templateBasePath()+"/css.html"
        return path
    def htmlPath(self):
        return self.templateBasePath()+"/html.html"
    def jsPath(self):
        path = self.templateBasePath()+"/js.html"
        return path
    def ajaxHandlerPost(self):
        return None
    def ajaxHandlerGet(self):
        return None
    def requestHandler(self):
        return None
    
class PluginRegistry(object):
    def __init__(self):
        self._registry = []

        for name in os.listdir(os.path.dirname(os.path.realpath(__file__))):
            if not os.path.isdir( os.path.join ( 
                                    os.path.dirname(os.path.realpath(__file__)),
                                    name )
                                    ):
                continue
            try:
                mod = __import__(globals()["__name__"]+"."+name, None, None, [''])
                self._registry.append(mod.init())
            except Exception, e:
                print "Plugin system: failed to import "+name
                import traceback
                print traceback.print_tb(sys.exc_traceback)

    
        print "Plugin system found the following plugins: "+str(self._registry)
    
    def allPlugins(self):
        return self._registry

    def pluginByName(self, name):
        plugins = [x for x in self._registry if x.name() == name]
        if len(p) == 0:
            return None
        if len(p) == 1:
            return p[0]
        raise Exception("Multiple plugins with name "+str(name))
        
def jsrender(request, plugin_name, file_name):
    registry = PluginRegistry()
    file_name = os.path.basename(file_name)
    all_plugins = registry.allPlugins()
    
    for p in registry.allPlugins():
        if p.name() == plugin_name:
            jsfile = os.path.join(p.basePath(),"files","js",file_name)

            c = template.Context({})
            t = loader.get_template(jsfile)
            return http.HttpResponse(t.render(c), mimetype="text/javascript");
    
    raise http.Http404

def cssrender(request, plugin_name, file_name):
    registry = PluginRegistry()
    file_name = os.path.basename(file_name)
    all_plugins = registry.allPlugins()
    
    for p in registry.allPlugins():
        if p.name() == plugin_name:
            cssfile = os.path.join(p.basePath(),"files","css",file_name)

            c = template.Context({})
            t = loader.get_template(cssfile)
            return http.HttpResponse(t.render(c), mimetype="text/css")
    
    raise http.Http404

def javarender(request, plugin_name, file_name):
    registry = PluginRegistry()
    file_name = os.path.basename(file_name)
    all_plugins = registry.allPlugins()
    
    for p in registry.allPlugins():
        if p.name() == plugin_name:
            javafile = os.path.join(p.basePath(),"files","java",file_name)
            f=file(javafile, "r")
            return http.HttpResponse(f.read(), mimetype="application/x-java-applet")
    
    raise http.Http404
