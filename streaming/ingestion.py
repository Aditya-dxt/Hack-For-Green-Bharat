import time
import random
import pathway as pw

class EnvSchema(pw.Schema):
    timestamp: float
    city: str
    aqi: int
    pm25: float
    pm10: float

# 1. The Data Generator
def env_event_stream():
    cities = ["Delhi", "Mumbai", "Bengaluru"]
    while True:
        yield {
            "timestamp": time.time(),
            "city": random.choice(cities),
            "aqi": random.randint(50, 400),
            "pm25": round(random.uniform(10, 300), 2),
            "pm10": round(random.uniform(20, 500), 2),
        }
        time.sleep(1)

# 2. The Connector Class (The missing piece!)
class StreamSubject(pw.io.python.ConnectorSubject):
    def run(self):
        # This loops over your generator and pushes data into Pathway
        for data in env_event_stream():
            self.next(**data)

def ingest_stream() -> pw.Table:
    print("DEBUG: Final version running - Class Implementation")

    # 3. Instantiate your custom subject
    subject = StreamSubject()

    return pw.io.python.read(
        subject,
        schema=EnvSchema,
        mode="streaming",
    )