import urlparse
import os
from . import utils

class FileStorage:
    def __init__(self, subpath, web_accessible, settings):
        if web_accessible:
            self._base_path = settings["WEB_CACHE_BASE_DIR"]
        else:
            self._base_path = settings["LOCAL_CACHE_BASE_DIR"]

        self._subpath = subpath
        self._web_accessible = web_accessible
        self._storage_path = os.path.join(self._base_path, self._subpath)
        self._web_base_url = settings["WEB_CACHE_WEB_BASE_URL"]
        if not os.path.exists(self._storage_path):
            os.makedirs(self._storage_path)

    def path(self, filename):
        return os.path.join(self._storage_path,filename)
    
    def url(self, filename):
        if not self._web_accessible:
            return None
        scheme, netloc, path, params, query, fragment = urlparse.urlparse(self._web_base_url)
        path = os.path.join(path, self._subpath, filename)
        return urlparse.urlunparse((scheme, netloc, path, params, query, fragment))

    def exists(self, filename):
        if os.path.exists(self.path(filename)):
            return True
        return False

    def readable(self, filename):
        return os.access(self.path(filename), os.R_OK)

class ResourceStorage(object):
    """Storage area for data associated to a specific resource"""
    def __init__(self, resource, web_accessible, settings):
        self._resource = resource
        self._file_storage = FileStorage( os.path.join("resources",utils.uriToUuid(self._resource.uri())), web_accessible, settings)
    
    def url(self, data_name, data_extension, parameters=None):
        if not parameters:
            return self._file_storage.url(data_name+"_"+utils.uriToUuid(self._resource.uri())+"."+data_extension)
        else:
            parameter_string = "_".join(map(lambda v: str(v[0])+"="+str(v[1]), parameters.items()))
            return self._file_storage.url(data_name+"_"+utils.uriToUuid(self._resource.uri())+"_"+parameter_string+"."+data_extension)

         
    def path(self, data_name, data_extension,parameters=None):
        if not parameters:
            return self._file_storage.path(data_name+"_"+utils.uriToUuid(self._resource.uri())+"."+data_extension)
        else:
            parameter_string = "_".join(map(lambda v: str(v[0])+"="+str(v[1]), parameters.items()))
            return self._file_storage.path(data_name+"_"+utils.uriToUuid(self._resource.uri())+"_"+parameter_string+"."+data_extension)

    def readable(self, data_name, data_extension, parameters=None):
        if not parameters:
            return self._file_storage.readable(data_name+"_"+utils.uriToUuid(self._resource.uri())+"."+data_extension)
        else:
            parameter_string = "_".join(map(lambda v: str(v[0])+"="+str(v[1]), parameters.items()))
            return self._file_storage.readable(data_name+"_"+utils.uriToUuid(self._resource.uri())+"_"+parameter_string+"."+data_extension)

class ResourceIcon(object):
    STATIC = "STATIC"
    ANIMATED = "ANIMATED"
    def __init__(self, resource, settings):
        self._resource = resource
        self._storage = ResourceStorage( resource, web_accessible=True, settings=settings)
    
    def url(self, icon_type=None):
        if not icon_type:
            icon_type = ResourceIcon.STATIC
        
        if icon_type == ResourceIcon.STATIC:
            return self._storage.url("icon", "png")
        elif icon_type == ResourceIcon.ANIMATED:
            return self._storage.url("animatedicon", "gif")
        else:
            raise ValueError("Invalid icon_type")

    def path(self, icon_type=None):
        if not icon_type:
            icon_type = ResourceIcon.STATIC

        if icon_type == ResourceIcon.STATIC:
            return self._storage.path("icon", "png")
        elif icon_type == ResourceIcon.ANIMATED:
            return self._storage.path("animatedicon", "gif")
        else:
            raise ValueError("Invalid icon_type")

    def readable(self, icon_type=None):
        if not icon_type:
            icon_type = ResourceIcon.STATIC

        if icon_type == ResourceIcon.STATIC:
            return self._storage.readable("icon", "png")
        elif icon_type == ResourceIcon.ANIMATED:
            return self._storage.readable("animatedicon", "gif")
        else:
            raise ValueError("Invalid icon_type")

