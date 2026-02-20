from services.alert_dispatcher import dispatch_alert
from models.alert_model import Alert
from streaming.env_stream import sensor_stream
from citizen.citizen_stream import citizen_stream
from integration.event_processor import process_event
from citizen.report_handler import process_citizen_report
from rag.engine import generate_rag_response


def print_system_banner():
    print("\n🌍 Hack For Green Bharat - Environmental Monitoring System")
    print("🔄 Streaming → Processing → RAG Intelligence → Alert Dispatch")
    print("-------------------------------------------------------------\n")




def handle_alert(alert):
   
    explanation = generate_rag_response(alert)
    dispatch_alert(alert, explanation)
    
    
def main():
     
    print_system_banner()

    try:
        for event in sensor_stream():

            alert = process_event(event)

            if alert:
                handle_alert(alert)
                
        for report in citizen_stream():
            
            
            citizen_alert = process_citizen_report(report)

            if citizen_alert:
                handle_alert(citizen_alert)
            
    except KeyboardInterrupt:
        print("\n🛑 System stopped manually.")


if __name__ == "__main__":
    main()

