class _configuration(type):
    @staticmethod
    def __getattr__(name):
        value = None
        if hasattr(configuration.config, name):
            value = getattr(configuration.config, name)
        elif hasattr(configuration.default, name):
            value = getattr(configuration.default, name)
        return value.format(appPath=configuration.appPath) if isinstance(value, str) else value


class configuration(metaclass=_configuration):
    __metaclass__ = _configuration

    @staticmethod
    def init(config, appPath):
        configuration.config = config
        configuration.default = deflautConfig()
        configuration.appPath = appPath


class deflautConfig:

    middleware_list = []

    middleware_path = "{appPath}/middleware"

    controller_path = "{appPath}/controller"

    plugin_path = "{appPath}/plugin"

    plugin_list = []

    filter_path = "{appPath}/filter"

    filter_list = []

    service_path = "{appPath}/service"

    util_path = "{appPath}/util"

    cors = "http://localhost"

    cookie_id = "alauda_app_id"

    encrypt = "keyskeyskeyskeys"

    router_controller = "home"

    router_action = "index"
