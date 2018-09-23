import warnings 

# this class violates on purpose coding practices of having a class with a capital letter.
# We do this because as a decorator, it looks better with a uncapitalized letter

class DeprecationWarning(Warning): pass

class deprecated(object):  
    def __init__(self, warning):  
        self._warning = warning  
    def __call__(self, function):  
        def f(*args, **kwargs):  
            warnings.warn("Deprecated method %s called. %s" %  (function.__name__, self._warning), category=DeprecationWarning, stacklevel=2)  
            return function(*args, **kwargs)  
        f.__name__ = function.__name__  
        f.__doc__ = function.__doc__  
        f.__dict__.update(function.__dict__)  
        return f

