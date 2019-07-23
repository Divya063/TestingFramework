
class Grafana:
    def __init__(self):
        self.success = None
        self.error = None
        self.emessage = None

    def set_success(self):
        self.success = True
        self.error = False

    def set_error(self, emsg=None):
        self.success = False
        self.error = True
        self.emessage = emsg

    # Performance utilities
    def set_performance(self, time):
        self.time_taken = time


    def make_stats_and_publish(self, test_class, monitoring_host, monitoring_port, to_grafana):
        # Scroll the list of WriteOp to collect statistics
        if to_grafana:
            self.publish_on_grafana()


    def publish_on_grafana(self):
        pass