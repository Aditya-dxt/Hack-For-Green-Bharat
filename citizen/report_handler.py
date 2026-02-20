from models.alert_model import Alert
import time

def process_citizen_report(report):
    """
    Converts citizen report into standard Alert object.
    """

    alert = Alert(
        event_type="CITIZEN_REPORT",
        location=report["location"],
        pm25=0,  # citizen may not know value
        severity="REPORTED",
        timestamp=time.time(),
        source="CITIZEN"
    )

   
    

    return alert

