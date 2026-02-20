from models.alert_model import Alert

THRESHOLD = 150

def process_event(data):

    pm25 = data["pm25"]

    if pm25 < 100:
        severity = "MODERATE"
    elif pm25 < 200:
        severity = "HIGH"
    else:
        severity = "CRITICAL"

    if pm25 >= THRESHOLD:

        alert = Alert(
            event_type="POLLUTION_SPIKE",
            location=data["location"],
            pm25=pm25,
            severity=severity,
            timestamp=data["timestamp"],
            source="SENSOR"
        )

       

        return alert

    else:
        print(f"✅ Normal Air in {data['location']} | PM2.5 = {pm25}")
        return None

