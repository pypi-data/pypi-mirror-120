import _thread
import time


class plugin:
    def run(self):
        pass

    def start(self, isOnce, interval):
        if not isOnce:
            _thread.start_new_thread(self._run, (interval,))
        else:
            self.run()

    def _run(self, interval):
        while True:
            self.run()
            time.sleep(interval)