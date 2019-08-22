class Grafana():
    """ Implements everything needed by grafana"""

    def __init__(self):
        self.success = None
        self.error = None
        self.emessage = None
        self.time_taken = None

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
        # Scroll the list  to collect statistic
        statistic = []
        for module in test_class.stats.values():
            statistic.append(module.success)
            statistic.append(module.time_taken)

        if to_grafana:
            # logic for pushing to grafana goes here
            print(statistic)


