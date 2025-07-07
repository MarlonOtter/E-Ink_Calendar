#import libraries
from Events import *
import json

# say the scope that the calendar will use (read/write data)
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

directory = "Files/Secrets/"

class GoogleCalendar:
    def __init__(self):
        self.check()
        self.Events = Events(self)
        self.calendarIds = []

    def addCalendar(self, id):
        if id:
            self.calendarIds.append(id)

    def check(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f"{directory}token.json"):
            self.creds = Credentials.from_authorized_user_file(f"{directory}token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{directory}credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(f"{directory}token.json", "w") as token:
                token.write(self.creds.to_json())


if __name__ == "__main__":
    cal = GoogleCalendar()
    
    #add the calendars
    with open(f"{directory}calendars.json", "r") as f:
        txt = f.readlines()
        jsonData = json.loads("".join(txt))
        if not jsonData:
            print("No calendars found in calendars.json")
            exit(1)
        for calendar in jsonData["calendars"]:
            print(f"Adding calendar: {calendar['name']}")
            cal.addCalendar(calendar["id"])
            
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

    