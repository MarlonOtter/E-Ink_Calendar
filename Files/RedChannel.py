# RedChannel.py
# This generates the red channel of the calendar image
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025

import MultiLineText as mlt

from PIL import Image,ImageDraw
import datetime as dt
import dateutil as du
import os

# Import all the required constants and methods from the general file
from CalendarUtils import FORMAT, DATEFONT, CURRENT_EVENTFONT, NEXT_EVENTFONT, ALLMONTHS, _CalendarPosition, _DrawCalendarBox, _SameDay, GetEventEndDate, GetEventStartDate

# Define the values for drawing in RED and WHITE
RED = 0
WHITE = 255
DATE = dt.datetime.today().date()

# define the image 
image = Image.new("1", (800, 480), WHITE)
imageDraw = ImageDraw.Draw(image)


def AddMainBox():
    pos = FORMAT["sideBox"]["pos"]
    size = FORMAT["sideBox"]["size"]
    imageDraw.rectangle((pos[0], pos[1], size[0], size[1]), fill=RED)


def AddDate():
    # Get the information from the json
    pos = FORMAT["sideBox"]["pos"]
    size = FORMAT["sideBox"]["size"]
    padding = FORMAT["sideBox"]["date"]["top"]

    # Adds the correct suffix to the date
    todayDay = int(str(DATE.day)[-1]) - 1
    suffixList = ["st", "nd", "rd",  "th"]
    
    # days that are larger than 3 should be "th"
    if todayDay > 3: todayDay = 3

    # If the day is 11, 12 or 13, it should be "th"
    if DATE.day == 11 or DATE.day == 12 or DATE.day == 13:
        todayDay = 3
        
    suffix = suffixList[todayDay]

    # Draw the text
    imageDraw.text(
        ((pos[0] + (size[0] // 2) - 15), (pos[1] + padding)),
        f"{DATE.day}{suffix} {ALLMONTHS[DATE.month-1]} {DATE.year}",
        fill=WHITE, 
        font=DATEFONT, 
        anchor="mm"
        )
    
    # Draw the Underline underneath the text
    top = FORMAT["sideBox"]["date"]["underline"]["top"]
    side = FORMAT["sideBox"]["date"]["underline"]["side"]

    imageDraw.line(
        ((pos[0] + side, pos[1] + padding + top), 
         (size[0] - side, pos[1] + padding + top)),
        fill=WHITE,
        width=3
        )
    

def AddWeather(weatherCode:str):
    if not weatherCode:
        return
    
    pos = FORMAT["sideBox"]["pos"]
    size = FORMAT["sideBox"]["size"]
    imageSize = FORMAT["sideBox"]["weather"]["size"]

    top = FORMAT["sideBox"]["weather"]["top"]
    
    weatherIcon = Image.open(os.path.join(os.path.dirname(__file__), "Assets", "Weather", f"{weatherCode[:-1]}d@4xR.png"))
    image.paste(
        weatherIcon,
        ((pos[0] + size[0]) // 2 - imageSize[0]//2, top)
        )


def AddEventInfo(events:dict, bins):
    # Get any events that are today
    # and the next event
    todayEvents = []
    nextEvent = None
    nextEventDate = None
    # Loop through all the events
    for event in events:
        # Get the start date
        eventStartDate = GetEventStartDate(event)
        eventEndDate = GetEventEndDate(event)
        
        # If it is today add it to the list
        #print(f"event: {event['summary']}, {eventStartDate}")
        if (eventStartDate.date() == DATE or (eventStartDate.date() < DATE and eventEndDate.date() > DATE)):
            todayEvents.append(event)
            
        # Go through all the events and get the next event
        if (eventStartDate.date() > DATE):
            if (nextEvent == None):
                nextEvent = event
                nextEventDate = eventStartDate
            else:
                #TODO: change to consider time aswell 
                if (eventStartDate.date() < nextEventDate.date()):
                    nextEvent = event
                    nextEventDate = eventStartDate
            
    
    # Draw the events that are today
    text = ""
     
    # Loop through all the events
    for item in todayEvents:
        # Get the description
        text += f"{item['summary']} \n"
    
    # add bin data if available
    if bins:    
        bin = bins.getTomorrow(DATE)
        if bin:
            text += f"\n{bin} bin \n"
    
    # if the description is longer than 20 characters, split it to seperate lines 
    textArray = (mlt.splitText(text, 20)).split(" \n")
    # Remove any empty lines if there are any
    try:
        textArray.remove(" ")
    except ValueError: pass
    
    pos = FORMAT["sideBox"]["pos"]
    size = FORMAT["sideBox"]["size"]
    boxMiddle = (pos[0] + size[0])//2
    currentEventTop = FORMAT["sideBox"]["currentEvent"]["top"]
    currentEventFontSize = FORMAT["sideBox"]["currentEvent"]["fontSize"]

    # Go through each line of text and draw it on the image
    for index, line in enumerate(textArray):
        line = line.replace("\n", "")
        imageDraw.text(
            (boxMiddle, currentEventTop + (index * currentEventFontSize)), 
            line, 
            fill=WHITE, 
            anchor="mm", 
            font=CURRENT_EVENTFONT
            )



    # Draw the upcoming event
    nextEventTop = FORMAT["sideBox"]["nextEvent"]["top"]
    
    # Only draw anything if there is an event
    if not nextEvent:
        return
    
    imageDraw.text(
        (boxMiddle, nextEventTop), 
        f"Next Event:\n{mlt.splitText(nextEvent.get('summary'), 20)}",
        fill=WHITE, 
        anchor="mm", 
        font=NEXT_EVENTFONT
        )


def HighlightToday():
    pos = _CalendarPosition(DATE.year, DATE.month, DATE.day-1)
    size = FORMAT["calendar"]["size"]
    padding = FORMAT["calendar"]["day"]["padding"]

    squareSize = [size[0]//7 - padding*2, size[1]//6 - padding*2]

    _DrawCalendarBox(imageDraw, pos, RED, WHITE, DATE.day)

def AddUpcomingEvents(events:dict):
    # loop through each event
    monthStart = dt.date(DATE.year, DATE.month, 1)
    monthEnd = monthStart + du.relativedelta.relativedelta(months=+1, days=-1)
    for event in events:
        startDT:dt.datetime = GetEventStartDate(event)
        endDT:dt.datetime = GetEventEndDate(event)
        
        # endDT is the next day if the event is set to be all day
        # so this fixes it so that it ends on the same day that it starts
        # so it doesn't spread across multiple days 
        isAllDay:bool = event["start"].get("date") is not None
        if isAllDay: 
            endDT += dt.timedelta(days=-1)
    
        # if event cannot be displayed
        # stop
        if (
            (startDT.date() > monthEnd) or
            (endDT.date() < monthStart)
            ):
            continue
        
       
        # move to the first of the month if the event starts in the previous month and ends in this or a later month
        if ((startDT.date().month < DATE.month) or (startDT.date().year < DATE.year)):
            startDT = dt.datetime(DATE.year, DATE.month, 1)
            
        # calculate the position of the square that is going to be 
        # For some reason I have to -1 from the day, problably to do with 0-indexed arrays or something 
        startPos = _CalendarPosition(startDT.year, startDT.month, startDT.day-1)
        endPos = _CalendarPosition(endDT.year, endDT.month, endDT.day-1)
        
        # Padding and size of the event icon 
        padding = FORMAT["calendar"]["events"]["padding"]
        sizeX = FORMAT["calendar"]["events"]["sizeX"]
        longSizeX = FORMAT["calendar"]["events"]["longSizeX"]
        sizeY = FORMAT["calendar"]["events"]["sizeY"]
        calSize = FORMAT["calendar"]["size"]

        # during the same week
        #print(f"startPos: {startPos}, endPos: {endPos}")
        if ((startPos[0] == endPos[0]) and (startPos[1] == endPos[1])):
            #print("0")
            _drawEventIcon(startPos, sizeX, sizeY, padding)
        elif (startPos[1] == endPos[1]):
            #print("1")
            _drawEventIcon(startPos, (endPos[0] - startPos[0]) + longSizeX, sizeY, padding)
        else:
            #print("2")
            # event covers multiple weeks
            week:int = 0 
            for i in range(0,6):
                mon:dt.datetime = startDT + dt.timedelta( days=-(startDT.isoweekday()-1) + week * 7)
                monPos = _CalendarPosition(mon.year, mon.month, mon.day-1)
                
                if _SameDay(mon, endDT):
                    #print("2.1")
                    _drawEventIcon(monPos, sizeX, sizeY, padding)
                    break
                
                sun:dt.datetime = mon + dt.timedelta(days=6)
                sunPos = _CalendarPosition(sun.year, sun.month, sun.day-1)
                
                if (week == 0):
                    #print("2.2")
                    if (not _checkEndOfMonth(startDT, startPos, sun, calSize, padding, sizeY)):
                        _drawEventIcon(startPos, (sunPos[0] - startPos[0]) + (calSize[0] // 7) - padding * 2, sizeY, padding)
                        week += 1
                        continue
                    break
                
                if _checkEndOfMonth(mon, monPos, sun, calSize, padding, sizeY):
                    break
                
                if endDT > sun:
                    #print("2.3")
                    # draw a box between mon and sun        
                    _drawEventIcon(monPos, (sunPos[0] - monPos[0]) + (calSize[0] // 7) - padding * 2, sizeY, padding)
                    week += 1
                    continue
                #print("2.4")
                
                _drawEventIcon(monPos, (endPos[0] - monPos[0]) + longSizeX, sizeY, padding)
                break


def _checkEndOfMonth(mon, monPos, sun, calSize, padding, sizeY):
    if (sun.month != mon.month):
        #print("2.5")
        lastDay = mon
        for i in range(1,6):
            temp = mon + dt.timedelta(days=i)
            if (temp.month != mon.month):
                break 
            lastDay = temp  
        #print(f"lastDayOfMonth: {lastDay.isoformat()}")    
        pos = _CalendarPosition(lastDay.year, lastDay.month, lastDay.day-1)
        _drawEventIcon(monPos, (pos[0] - monPos[0]) + (calSize[0] // 7) - padding * 2, sizeY, padding)
        return True
    return False        

def _drawEventIcon( pos, sizeX:int, sizeY:int, padding:int):    
    imageDraw.rectangle(
        (pos[0] + padding, pos[1] + padding, pos[0] + sizeX + padding, pos[1] + sizeY + padding),
        outline=0,
        width=8,
        fill=RED
        )


def Draw(weather:str, events:dict, bins):
    #Reset the images
    global image, imageDraw
    image = Image.new("1", (800, 480), WHITE)
    imageDraw = ImageDraw.Draw(image)

    AddMainBox()
    AddDate()
    AddWeather(weather)
    AddEventInfo(events, bins)
    HighlightToday()
    AddUpcomingEvents(events)
    return image


if __name__ == "__main__":
    # Example weather and event data
    weather = "09d"
    events = [
  {
    "summary": "Test event",
    "start": {
      "date": "2025-07-15"
    },
    "end": {
      "date": "2025-07-11"
    }
  }
]

    Draw(weather, events)
    image.save("Output/red_channel.png")
