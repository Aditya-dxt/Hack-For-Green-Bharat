import time
import random
import json


def live_environmental_stream():
    """
    Simulates live environmental sensor data in real time.
    Emits one event per second.
    """
    while True:
        event = {
            "timestamp": int(time.time()),
            "city": "Delhi",
            "pm25": round(random.uniform(30, 300), 2),
            "pm10": round(random.uniform(50, 400), 2),
            "no2": round(random.uniform(10, 150), 2),
        }

        yield json.dumps(event).encode("utf-8")
        time.sleep(1)
