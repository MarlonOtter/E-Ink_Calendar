# main.py
# This is the main file that runs the calendar and display program
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025

import os
import datetime as dt
from multiprocessing.pool import ThreadPool

import APIs.SendErrorEmail as sendErrorEmail

# Some validation so that this file can be ran on windows/devices without the display connected
importedScreenLib = True
try:
    from waveshare_epd import epd7in5b_V2
except:
    print("ERROR LOADING 'waveshare_epd' LIBRARY")
    importedScreenLib = False

epd = None

apiData = ""

# List of all extra files that are needed for the program to run (non-code)
REQUIREDFILES = [
        "format.json",
        "APIs/secrets/GoogleCalendar/credentials.json",
        "APIs/secrets/GoogleCalendar/token.json",
        "APIs/secrets/OpenWeatherMap/key.json",
        "APIs/secrets/GoogleCalendar/calendars.json",
        "APIs/secrets/email.json",
        "Assets/FreeSans.ttf",
        "Assets/Weather", # All the weather images in the directory
    ]

# Make sure that all the required files exist
def CheckFiles():
    missingFile = False

    # Loop through all the required files
    for file in REQUIREDFILES:
        # If it is missing output an error
        if not os.path.exists(file):
            missingFile = True
            print(f"ERROR: Missing File '{file}'")
    # Exiting here instead of in the loop means that all the missing files are anounced instead of one at a time
    if missingFile:
        return -1
    return 0

def GetData():
    global apiData
    import FetchApiData as APIs
    
    pool = ThreadPool(processes=2)
    asyncWeather = pool.apply_async(APIs.GetWeather)
    asyncEvents = pool.apply_async(APIs.GetCalendar, (dt.datetime.today(),))

    events = asyncEvents.get()
    weather = asyncWeather.get()

    apiData = (weather, events)
    
    return weather, events


# Setup and clear the display
def SetupHardware():
    global epd
    epd = epd7in5b_V2.EPD()
    epd.init()
    epd.Clear()

# Generate the Red Channel of the calendar to be displayed
def GenerateRed(weather, events):
    import RedChannel as RC
    RC.Draw(weather, events)
    
    return RC.image.rotate(180)

# Generate the Black Channel of the calendar to be displayed
def GenerateBlack(weather):
    import BlackChannel as BC
    BC.Draw(weather)
    
    return BC.image.rotate(180)

# Display the calendar on the screen
def DisplayImage(red, black):

    epd.display(epd.getbuffer(black), epd.getbuffer(red))

# Put the display to sleep
def Complete():
    epd.sleep()


def Run():
    # Make sure all the files that are required are accessable before running the program
    if CheckFiles() == -1: 
        raise ImportError("Missing Files required to run program")

    pool = ThreadPool(processes=2)

    # Setup Hardware asynchronously as it can take a while
    if importedScreenLib:
        asyncSetup = pool.apply_async(SetupHardware)

    # Make the API calls
    start = dt.datetime.now()
    weather, events = GetData()
    print("API Requests Took: ", dt.datetime.now() - start)

    black = GenerateBlack(weather)
    red = GenerateRed(weather, events)
    

    # Display the images on the screen
    if importedScreenLib:
        asyncSetup.get()
        DisplayImage(red, black)
        Complete()
    else:
        red.save("Output/red_channel.png")
        black.save("Output/black_channel.png")
        pass

if __name__ == "__main__":
    start = dt.datetime.now()
    try:
        Run()
    except Exception as e:
        date = dt.datetime.now()
        weather = "N/A"
        events = "N/A"
        if apiData:
            weather = apiData[0]
            events = apiData[1]
        subject, body = sendErrorEmail.GenerateMessage(date, weather, events, e)
        sendErrorEmail.sendEmail(subject, body)
        print("Sent ERROR message to Email")
    
    print("Total Time Taken: ", dt.datetime.now() - start)