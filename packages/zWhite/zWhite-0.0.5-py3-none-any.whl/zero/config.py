class configuration:
    @staticmethod
    def init(config, appPath):
        configuration.config = config
        configuration.default = deflautConfig()
        configuration.appPath = appPath

    @staticmethod
    def __getattr__(name):
        value = None
        if hasattr(configuration.config, name):
            value = getattr(configuration.config, name).format(appPath=configuration.appPath)
        elif hasattr(configuration.default, name):
            value = getattr(configuration.default, name).format(appPath=configuration.appPath)
        return value

class deflautConfig:

    middleware_list = []

    middleware_path = "{appPath}/middleware"

    controller_path = "{appPath}/controller"

    plugin_path = "{appPath}/plugin"

    filter_path = "{appPath}/filter"

    core = "*"

    cookie_id = "alauda_app_id"

    encrypt = "keyskeyskeyskeys"

    router_controller = "home"

    router_action = "index"