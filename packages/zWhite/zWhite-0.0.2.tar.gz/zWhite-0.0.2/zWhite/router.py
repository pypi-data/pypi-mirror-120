from .config import configuration

class router():
    def __init__(self, url):
        urls = url.split("?")[0].split("/")
        self.controller = configuration.router_controller
        self.action = configuration.router_action
        if len(urls) == 2:
            self.controller = urls[1]
        elif len(urls) == 3:
            self.controller = urls[1]
            self.action = urls[2]
