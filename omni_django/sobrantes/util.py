from types import ModuleType

class abstractclassmethod(classmethod):
    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


def on_gae_platform():
    try:
        import google.appengine.ext.ndb as ndb
        return isinstance(ndb, ModuleType)
    except:
        return False


def singleton(cls):
    instance = cls()
    result = lambda: instance
    result.__doc__ = cls.__doc__
    return result


def ensure_extension(filename, extension):
    extension = '.%s' % extension
    if not filename.endswith(extension):
        filename += extension
    return filename
