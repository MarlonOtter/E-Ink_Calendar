# FetchApiData.py
# Makes the various requests to APIs for the calendar to display
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025


import APIs.googleCalendarAPI as gooCal
import APIs.GetForcastWeather as weather
import json
import datetime as dt
import calendar as cal
import os

calendar = None

def setupCalendar():
    global calendar
    # Load the Calendars from the external file
    calendar = gooCal.GoogleCalendar()
    if (calendar.setup == False):
        return
    
    CALENDARS_LIST = os.getenv("GOOGLE_CALENDAR_CALENDARS")
    if (CALENDARS_LIST == None):
        raise ValueError("Calendars not defined despite calendar feature being enabled")
    
    calendars = CALENDARS_LIST.split("\n")
    for cal in calendars:
        id = cal.split(", ")
        if (len(id) >= 2):
            calendar.addCalendar(id[1])


def GetWeather():
    data = weather.GetForcast()
    if (data == None):
        return None
    return data[2]

def GetCalendar(date):
    if (calendar == None):
        setupCalendar()
    if (not calendar.setup):
        return []
    events = calendar.Events.getWithin(dt.datetime(date.year, date.month, 1), date + dt.timedelta(days=cal.monthrange(date.year, date.month)[1]))
    return events

def GetBins():
    import APIs.BinsAPI as bin
    binDates = bin.getNextBinDates()
    return binDates

if __name__ == "__main__":
    # Get the Weather
    weatherCode = GetWeather()
    print("Code: " + weatherCode or "none")

    # Get the calendar
    events = GetCalendar(dt.datetime.now())
    print("events: ", events)
    
    bins = GetBins()
    print(bins.to_string(bins.black))