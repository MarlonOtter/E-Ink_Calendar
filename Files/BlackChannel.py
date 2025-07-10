# BlackChannel.py
# This generates the black channel of the calendar image
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025


from PIL import Image,ImageDraw
import calendar as cal
import os
import datetime as dt

from CalendarUtils import FORMAT, WEEKDAYFONT, ALLDAYS, REDONLY_WEATHER, _CalendarPosition, _DrawCalendarBox

BLACK = 0
WHITE = 255
DATE = dt.datetime.today()

# Define the image 
image = Image.new("1", (800, 480), WHITE)
imageDraw = ImageDraw.Draw(image)


def AddCalendarBoxes():
    daysInMonth = cal.monthrange(DATE.year, DATE.month)[1]
    size = FORMAT["calendar"]["size"]
    padding = FORMAT["calendar"]["day"]["padding"]

    boxSize = [size[0]//7 - padding*2, size[1]//6 - padding*2]

    for i in range(0, daysInMonth):
        # If the day is today then don't draw the box in black as it will be hidden by the red
        if i+1 == DATE.day: 
            continue

        # Calculate the position of the box
        # For some reason has to be 0-indexed for the day not sure why
        pos = _CalendarPosition(DATE.year, DATE.month, i)  
        # Then Draw the box at that location
        _DrawCalendarBox(imageDraw, pos, WHITE, BLACK, i+1)


def AddDaysOfWeek():
    pos = FORMAT["calendar"]["pos"]
    size = FORMAT["calendar"]["size"]
    top = FORMAT["calendar"]["weekday"]["top"]
    padding = FORMAT["calendar"]["day"]["padding"]

    boxWidth = (size[0]//7)

    for i in range(7):
        imageDraw.text(
            # For some reason I have to add 30 for it to line up no idea why
            (pos[0] + 30 + padding + (boxWidth)*i , top), 
            ALLDAYS[i], 
            font = WEEKDAYFONT,
            fill = 0, 
            anchor= "mm")
                

def AddWeather(weatherCode:str):
    if not weatherCode:
        return

    # If there isn't a black channel for the icon skip
    if weatherCode[:-1] in REDONLY_WEATHER:
        return
    
    # Get the icon
    weatherIcon = Image.open(os.path.join(os.path.dirname(__file__), "Assets", "Weather", f"{weatherCode[:-1]}d@4xB.png"))

    pos = FORMAT["sideBox"]["pos"]
    size = FORMAT["sideBox"]["size"]
    imageSize = FORMAT["sideBox"]["weather"]["size"]
    top = FORMAT["sideBox"]["weather"]["top"]

    # Draw it
    image.paste(
        weatherIcon,
        ((pos[0] + size[0]) // 2 - imageSize[0]//2, top)
        )




def Draw(weatherCode:str):
    #Reset the images
    global image, imageDraw
    image = Image.new("1", (800, 480), WHITE)
    imageDraw = ImageDraw.Draw(image)

    AddCalendarBoxes()
    AddDaysOfWeek()
    AddWeather(weatherCode)
    return image



if __name__ == "__main__":
    Draw("09d")
    image.save("Output/black_channel.png")
    