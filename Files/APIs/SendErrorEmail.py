import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json
import os
import datetime as dt

def GenerateMessage(date:dt.datetime, weather, events, err):
    # Email content
    subject = "ERROR with E-ink Calendar"
    body = f"""
    This is an automated message that is sent when the e-ink calendar encounters an error:

    The error that occured is:
    {err}

    Error Generating calendar for date:
    {date.isoformat()}.
    
    The weather code was: 
    {weather}
    
    Events Data is: 
    {json.dumps(_cleanEventData(events), indent=4)}    
    
    """
    return subject, body

def GenerateErrorMessage(err):
    # Email content
    subject = "ERROR with E-ink Calendar"
    body = f"""
    This is an automated message that is sent when the e-ink calendar encounters an error:

    The error that occured is:
    {err}
    """
    return subject, body

def sendEmail(subject, body):
    EMAILS_ENABLED = os.getenv("FEATURE_EMAIL_ON_FAIL")
    if (EMAILS_ENABLED != "ENABLED"):
        return
    
    SENDER_ADDRESS = os.getenv("EMAIL_SENDER_ADDRESS")
    APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
    RECEVIER_ADDRESS = os.getenv("EMAIL_RECIEVER_ADDRESS")
    
    # if missing data don't send an email as it is not possible
    if not SENDER_ADDRESS or not APP_PASSWORD or not RECEVIER_ADDRESS:
        return -1; 
    
    # Create message
    message = MIMEMultipart()
    message["From"] = SENDER_ADDRESS
    message["To"] = RECEVIER_ADDRESS
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send email via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_ADDRESS, APP_PASSWORD)
        server.sendmail(SENDER_ADDRESS, RECEVIER_ADDRESS, message.as_string())
        
    return 1

def _cleanEventData(events):
    result = []
    try:
        for event in events:
            # get name, start, end
            eventInfo = {
                "summary": event["summary"],
                "start": event["start"].get("date") or event["start"].get("dateTime"),
                "end": event["end"].get("date") or event["end"].get("dateTime"),
            }
            result.append(eventInfo)
    except Exception as e:
        return [f"Parse Error (events not in exepected format): {e}", events]
        
    return result

if __name__ == "__main__":
    print("Generating Message")
    subject, body = GenerateMessage(dt.datetime.today(), "09d", {"123" : "abc"}, "Test Email")
    sendEmail(subject, body)
    print("SENT")