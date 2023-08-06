from .config import configuration


class _service(type):
    serviceList = {}

    def __getattr__(self, name):
        if name not in _service.serviceList:
            module = getattr(__import__("{service}.{name}".format(service=configuration.service_path.replace(configuration.appPath, "").lstrip("/").replace("/", "."), name=name)), name)
            service = getattr(module, name)()
            _service.serviceList[name] = service
        return _service.serviceList[name]


class service(metaclass=_service):
    pass
