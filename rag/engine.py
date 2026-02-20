# Simulated environmental knowledge base



KNOWLEDGE_BASE = {
    "PM25_LIMIT": 60,
    "HEALTH_EFFECTS": "High PM2.5 exposure can cause respiratory diseases, asthma, and long-term lung damage.",
    "REGULATION": "According to CPCB standards, PM2.5 levels above 60 are considered unhealthy."
}


def retrieve_context(alert):
    """
    Simulates document retrieval based on alert type.
    """
    
    #  # For sensor alerts → return pollution knowledge
    if alert.source == "SENSOR":
     return {
        "safe_limit": KNOWLEDGE_BASE["PM25_LIMIT"],
        "health_info": KNOWLEDGE_BASE["HEALTH_EFFECTS"],
        "regulation_info": KNOWLEDGE_BASE["REGULATION"]
    }
   # For citizen alerts → minimal context
    elif alert.source == "CITIZEN":
        return {
            "action": "Authorities should verify the report and take necessary action."
        }

    # Fallback
    return {}
   
def generate_explanation(alert, context):
    """
    Generates explanation using alert + retrieved context.
    """


    # Severity  Warning
    
    if alert.severity == "CRITICAL":
        warning = "Immediate action is required."
    elif alert.severity == "HIGH":
        warning = "Preventive measures should be taken."

        
    else:
        warning = ""

    
    # SENSOR BASED ALERT
    
    if alert.source == "SENSOR":
        return (
            f"Air quality in {alert.location} is classified as {alert.severity}. "
            f"Current PM2.5 level is {alert.pm25}. "
            f"The safe limit is {context['safe_limit']}. "
            f"{context['regulation_info']} "
            f"{context['health_info']} "
            f"{warning}"
        )

   
    
    # CTIZEN BASED ALERT
   
    
    elif alert.source == "CITIZEN":
        return (
            f"A citizen has reported an environmental issue in {alert.location}. "
            f"Severity status: {alert.severity}. "
            f"{context.get('action', '')} "
            f"{warning}"
        )

  
   
    
    #  Fallback
   
    
    return "An environmental alert has been generated. Further investigation is required."




        
       
    
    
def generate_rag_response(alert):
    """
    Complete RAG pipeline:
    1. Retrieve context
    2. Generate explanation
    """

    context = retrieve_context(alert)
    explanation = generate_explanation(alert, context)
    return explanation


    




