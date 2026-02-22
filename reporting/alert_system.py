def trigger_alert(alert, explanation):
    """
    Responsible for final alert presentation.
    Can later be extended to:
    - Email
    - SMS
    - Dashboard
    - Database storage
    """

    print("\n🚨 FINAL ALERT 🚨")
    print("Location:", alert["location"])
    print("PM2.5 Level:", alert["pm25"])
    print("Severity:", alert["severity"])
    
    
    print("\n🧠 AI EXPLANATION:")
    print(explanation)
    
    print("\n")
   
