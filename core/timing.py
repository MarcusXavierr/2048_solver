from time import time_ns, sleep

class Delay:
    def __init__(self):
        self.last_timestamp = time_ns()

    def _ms_to_ns(self, ms: float):
        return ms * 1_000_000

    def _ns_to_seconds(self, ns: float):
        return ns / 1_000_000_000

    def start_tracking(self):
        self.last_timestamp = time_ns()

    def delay_with_compensation_ms(self, delay: float):
        current_timestamp = time_ns()
        time_to_wait = self._ms_to_ns(delay) - (current_timestamp - self.last_timestamp)
        if time_to_wait > 0:
            sleep(self._ns_to_seconds(time_to_wait))
        self.last_timestamp = time_ns()

