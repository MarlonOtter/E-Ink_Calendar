# CalendarUtils.py
# This contains methods and constants used across multiple files 
#   so that they don't have to be redeclared in multiple places
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025

import json 
import calendar as cal
from PIL import ImageFont
import datetime as dt
import os

path = os.path.dirname(__file__)

# Read the format data from the file
# Just a json file with a bunch of numbers
FORMAT = ""
with open(os.path.join(path, "format.json"), "r") as f:
    FORMAT = json.load(f)
    


# All the fonts
# Uses format.json for all of its information
DATEFONT = ImageFont.truetype(
    os.path.join(path, 'Assets', FORMAT['sideBox']['date']['font']),
    FORMAT["sideBox"]["date"]["fontSize"]
    )

CURRENT_EVENTFONT = ImageFont.truetype(
    os.path.join(path, 'Assets', FORMAT['sideBox']['currentEvent']['font']),
    FORMAT["sideBox"]["currentEvent"]["fontSize"]
    )

NEXT_EVENTFONT = ImageFont.truetype(
    os.path.join(path, 'Assets', FORMAT['sideBox']['nextEvent']['font']),
    FORMAT["sideBox"]["nextEvent"]["fontSize"]
    )

DAYFONT = ImageFont.truetype(
    os.path.join(path, 'Assets', FORMAT['calendar']['day']['font']), 
    FORMAT["calendar"]["day"]["fontSize"]
    )

WEEKDAYFONT = ImageFont.truetype(
    os.path.join(path, 'Assets', FORMAT['calendar']['weekday']['font']), 
    FORMAT["calendar"]["weekday"]["fontSize"]
    )


ALLDAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] 
ALLMONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

REDONLY_WEATHER = ["01", "02", "03", "13", "50"]


# subprocedure that calculates the position of the provided day on the calendar
def _CalendarPosition(year:int, month:int, day:int):
    pos = FORMAT["calendar"]["pos"]
    size = FORMAT["calendar"]["size"]

    # Get an array of all the weeks that make up the month
    weeks = cal.Calendar().monthdatescalendar(year, month)

    # Calculate where the days of this month start
    for i, weekDay in enumerate(weeks[0]):
        if weekDay.month == month:
            firstDay = i + 1
            break
            
    # identify the week that it is likely in
    week = day // 7

    # calculate how many more days to offset by
    daysRemainder = day % 7
    # If the day of the week is greater than 7 move onto the next week
    if firstDay + daysRemainder > 7:
        daysRemainder -= 7
        # Apply an extra week offset
        week += 1
        

    # Calculate the position in the week that the day is
    dayOfWeek = (firstDay + daysRemainder)

    # calculate the size of each square on the 7x6 grid
    squareSize = [size[0] // 7, size[1] // 6]

    # Calculate position of the square
    return [pos[0] + squareSize[0] * (dayOfWeek - 1), pos[1] + squareSize[1] * week]



def _DrawCalendarBox(imageDraw, pos, boxFill:int, textFill:int, day:str):
    size = FORMAT["calendar"]["size"]
    padding = FORMAT["calendar"]["day"]["padding"]
    boxSize = [size[0]//7 - padding*2, size[1]//6 - padding*2]

    # Draw the square
    imageDraw.rectangle(
        (pos[0] + padding, pos[1] + padding, pos[0] + padding + boxSize[0], pos[1] + padding + boxSize[1]), 
        outline = 0, 
        width=3, 
        fill=boxFill
        )
            
    # Draw the day number
    imageDraw.text(
        (pos[0] + (padding + boxSize[0])//2, pos[1] + (padding + boxSize[1])//2), 
        f"{day}", 
        font=DAYFONT, 
        fill=textFill, 
        anchor="mm"
        )

def _SameDay(a:dt.datetime, b:dt.datetime):
    return (a.year == b.year and a.month == b.month and a.day == b.day)

def GetEventStartDate(event):
    try:
        isoString:str = event["start"].get("date") or event["start"].get("dateTime")
        return dt.datetime.fromisoformat(isoString.replace("Z", "+00:00"))
    except Exception as e:
        return dt.datetime.today() + dt.timedelta(days=-31)

def GetEventEndDate(event):
    try:
        isoString:str = event["end"].get("date") or event["end"].get("dateTime")
        return dt.datetime.fromisoformat(isoString.replace("Z", "+00:00"))
    except Exception as e:
        return dt.datetime.today() + dt.timedelta(days=+3)
