class Alert:
    def __init__(self, event_type, location, pm25, severity, timestamp, source):
        self.event_type = event_type
        self.location = location
        self.pm25 = pm25
        self.severity = severity
        self.timestamp = timestamp
        self.source = source

    def to_dict(self):
        return {
            "event_type": self.event_type,
            "location": self.location,
            "pm25": self.pm25,
            "severity": self.severity,
            "timestamp": self.timestamp,
            "source": self.source
        }
