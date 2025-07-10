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

forcast = weather.Forcast()
calendar = gooCal.GoogleCalendar()

# Load the Calendars from the external file
with open(os.path.join(os.path.dirname(__file__), "APIs", "secrets", "GoogleCalendar", "calendars.json"), "r") as f:
    jsonText = f.readlines()
    jsonData = json.loads("".join(jsonText))
    if not jsonData:
        print("ERROR: No calendars found in calendars.json")
        exit(1)
    for calendarItem in jsonData["calendars"]:
        calendar.addCalendar(calendarItem["id"])
        print(f"Adding calendar: {calendarItem['name']}")

def GetWeather():

    start = dt.datetime.now()
    data = forcast.getForcast()
    print(f"Weather Request Took: {dt.datetime.now() - start}")

    return data[2]

def GetCalendar(date):
    start = dt.datetime.now()
    events = calendar.Events.getWithin(dt.datetime(date.year, date.month, 1), date + dt.timedelta(days=cal.monthrange(date.year, date.month)[1]))
    print(f"google Calendar Request Took: {dt.datetime.now() - start}")
    return events

if __name__ == "__main__":
    # Get the Weather
    weatherCode = GetWeather()
    print("Code: " + weatherCode or "none")

    # Get the calendar
    events = GetCalendar()
    print("events: ", events)