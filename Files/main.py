# main.py
# This is the main file that runs the calendar and display program
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025

import os

# Some validation so that this file can be ran on windows/devices without the display connected
importedScreenLib = True
try:
    from waveshare_epd import epd7in5b_V2
except:
    print("ERROR LOADING 'waveshare_epd' LIBRARY")
    importedScreenLib = False


epd = None

# List of all extra files that are needed for the program to run (non-code)
REQUIREDFILES = [
        "format.json",
        "APIs/secrets/GoogleCalendar/credentials.json",
        "APIs/secrets/GoogleCalendar/token.json",
        "APIs/secrets/OpenWeatherMap/key.json",
        "calendars.json",
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
    import FetchApiData as APIs
    weather = APIs.GetWeather()
    events = APIs.GetCalendar()
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
    return RC.image

# Generate the Black Channel of the calendar to be displayed
def GenerateBlack(weather):
    import BlackChannel as BC
    BC.Draw(weather)
    return BC.image

# Display the calendar on the screen
def DisplayImage(red, black):
    epd.display(epd.getbuffer(black), epd.getbuffer(red))

# Put the display to sleep
def Complete():
    epd.sleep()
    epd7in5b_V2.epdconfig.module_exit()


def Run():
    # Make sure all the files that are required are accessable before running the program
    if CheckFiles() == -1: return

    # Make the API calls
    weather, events = GetData()

    # Generate the images
    red = GenerateRed(weather, events)
    black = GenerateBlack(weather)

    # Run all the Hardware stuff
    if importedScreenLib:
        SetupHardware()
        DisplayImage(red, black)
        Complete()
    else:
        # Or show the images if the hardware stuff doesn't work
        red.show()
        black.show()

if __name__ == "__main__":
    Run()