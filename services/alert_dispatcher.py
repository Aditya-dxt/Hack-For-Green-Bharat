from utils.logger import log_event

alert_count = 0  # Global alert counter


def dispatch_alert(alert, explanation):
    global alert_count
    alert_count += 1

    print("\n======================================================")
    print("🚨 ENVIRONMENTAL INTELLIGENCE ALERT 🚨")
    print("======================================================")

    print(f"Alert ID : {alert_count}")
    print(f"Source   : {alert.source}")
    print(f"Location : {alert.location}")
    print(f"Severity : {alert.severity}")

    if alert.source == "SENSOR":
        print(f"PM2.5    : {alert.pm25}")

    print("------------------------------------------------------")
    print("🧠 AI INSIGHT:")
    print(explanation)
    print("------------------------------------------------------")

    print("✔ Alert dispatched & logged successfully")
    print("======================================================\n")

    # Logging
    log_event(
        f"Alert ID {alert_count} | {alert.location} | {alert.severity} | Source: {alert.source}"
    )

