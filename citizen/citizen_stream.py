import time
import random

def citizen_stream():
    locations = ["Delhi", "Mumbai", "Jaipur"]
    issues = ["garbage", "smoke", "water_pollution"]

    while True:
        time.sleep(5)

        yield {
            "location": random.choice(locations),
            "issue_type": random.choice(issues),
            "description": "Reported by local citizen"
        }
