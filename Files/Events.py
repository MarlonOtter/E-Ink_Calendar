#import libraries
import datetime as dt
import os.path
import traceback

#import all google libaries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Events:
    def __init__(self, cal):
        self.cal = cal
        self.lastData = []

    # Public
    def _getNext(self, maxResults, start=0):
        allEvents = []
        for i in range(0, len(self.cal.calendarIds)):
            events = self._request(_calendarIndex = i, _start=start, _maxResults=maxResults)
            if events:
                allEvents.extend(events)
        allEvents = self._sortByDateTime(allEvents)
        if len(allEvents) >= maxResults:
            return allEvents[0::maxResults]
        return allEvents
        

    def getWithin(self, start, end):
        allEvents = []
        for i in range(0, len(self.cal.calendarIds)):
            events = self._request(_calendarIndex = i, _start=start, _end=end)
            if events:
                allEvents.extend(events)

        for i in range(len(allEvents)-1):
            if(allEvents[i]["start"].get("date")) == None:
                pass#allEvents.pop(i)
        
        try:
            self.lastData = self._sortByDateTime(allEvents)
            return self.lastData
        except TypeError as e:
            print("Type ERROR")
            traceback.print_exc()
            return []

    def next(self, date = dt.datetime.now()):
        for event in self.lastData:
            start = self._getDateTime(event)
            if start > date:
                return event
            #else: look at next event
        #if no event return nothing
        return
    
    def isEvent(self, date = dt.datetime.now(dt.timezone.utc)):
        events = []
        date = date
        for i, event in enumerate(self.lastData):
            start = self._getDateTime(event)
            if start.date() == date.date():
                events.append([i, event])
            if start.date() > date.date():
                return events
            #else: look at next event
        #if nothing
        return events


    # Private
    def _request(self, _calendarIndex=0, _start=0, _end=0, _maxResults=0):
        #set the value of any if they are not passed in
        if (_start == 0):
            _start = dt.datetime.now(dt.timezone.utc)
        if (_end == 0):
            _end = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=365)
        if (_maxResults == 0):
            _maxResults = 100

        def format_rfc3339(dt_obj):
            dt_obj = dt_obj.replace(microsecond=0)
            # If UTC, use 'Z'
            if dt_obj.tzinfo == dt.timezone.utc:
                return dt_obj.isoformat().replace('+00:00', 'Z')
            # If naive, assume UTC and add 'Z'
            if dt_obj.tzinfo is None:
                return dt_obj.isoformat() + 'Z'
            return dt_obj.isoformat()

        try:
            service = build("calendar", "v3", credentials=self.cal.creds)

            # Call the Calendar API          
            events_result = (
                service.events()
                .list(
                    calendarId=self.cal.calendarIds[_calendarIndex],
                    timeMin= format_rfc3339(_start),
                    timeMax= format_rfc3339(_end),
                    maxResults=_maxResults,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            return events_result.get("items", [])
            

        except HttpError as error:
            print(f"An error occurred: {error}")
        
    def _sortByDateTime(self, arr):
        #Bubble sort because im lazy
        swapped = True
        while swapped:
            swapped = False
            for i in range(0, len(arr)-2):
                A = self._getDateTime(arr[i])
                B = self._getDateTime(arr[i+1])
                if A > B:
                    arr[i], arr[i+1] = arr[i+1], arr[i]
                    swapped = True

        return arr
    
    def _getDateTime(self, event):
        date_str = event["start"].get("dateTime") or event["start"].get("date") or event["start"].get("Date")

        if date_str is None:
            print("ERROR: no date found in event")
            return dt.datetime(2007, 6, 28, tzinfo=dt.timezone.utc)
        
        if "T" not in date_str:
            date_str = date_str + "T00:00:00+00:00"
        # If it ends with Z, replace with +00:00 for fromisoformat
        if date_str.endswith("Z"):
            date_str = date_str[:-1] + "+00:00"
        return dt.datetime.fromisoformat(date_str)