# googleCalendarAPI.py
# makes requests to the Google Calendar API to get data such as stored events 
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025

from APIs.Events import *
import json

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# say the scope that the calendar will use (read/write data)
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

directory = os.path.join(os.path.dirname(__file__), "secrets", "GoogleCalendar")

class GoogleCalendar:
    def __init__(self):
        self.setup = False
        
        CALENDAR_ENABLED = os.getenv("FEATURE_GOOGLE_CALENDAR_EVENTS")
        if (CALENDAR_ENABLED != "ENABLED"):
            return
        
        self.check()
        self.Events = Events(self)
        self.calendarIds = []
        self.setup = True

    # Add the provided calendar to the list of calendars that will be searched
    def addCalendar(self, id):
        if id:
            self.calendarIds.append(id)

    # 
    def check(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(os.path.join(directory, "token.json")):
            self.creds = Credentials.from_authorized_user_file(os.path.join(directory, "token.json"), SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(directory, "credentials.json"), SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(os.path.join(directory, "token.json"), "w") as token:
                token.write(self.creds.to_json())


if __name__ == "__main__":
    cal = GoogleCalendar()
    
    #TODO GET THE .ENV
    
    CALENDARS_LIST = os.getenv("GOOGLE_CALENDAR_CALENDARS")
    if (CALENDARS_LIST == None):
        raise ValueError("Calendars not defined despite calendar feature being enabled")
    
    calendars = CALENDARS_LIST.split("\n")
    for cal in calendars:
        id = cal.split(", ")
        if (len(id) >= 2):
            cal.addCalendar(id[1])
            
    today = dt.datetime.today()
    start = dt.datetime(today.year, today.month, 1)
    end = today + dt.timedelta(days=30)
    print("Fetching events from calendars...")
    events = cal.Events.getWithin(start, end)

    if not events:
        print("No events found in the next 30 days.")
        exit(0)
    if events:
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(f"{start}, {event['summary']}")

    