from .config import configuration


class _util(type):
    utilList = {}

    def __getattr__(self, name):
        if name not in _util.utilList:
            module = getattr(__import__("{service}.{name}".format(service= configuration.util_path.replace(configuration.appPath, "").lstrip("/").replace("/", "."), name=name)), name)
            util = getattr(module, name)
            _util.utilList[name] = util
        return _util.utilList[name]()


class util(metaclass=_util):
    pass
