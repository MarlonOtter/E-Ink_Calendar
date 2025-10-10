# Tests.py
# Has a range of tests to test that the calendar displays the correct data
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025

import datetime as dt
import Simulate as sim
import json
import multiprocessing as mp

import os 
import sys

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

WEATHER_TYPES = ["01d", "02d", "03d", "04d", "09d", "10d", "11d", "13d", "50d"]


def TestAllDates():
    # Get the year that the user wants to be tested
    year = input("Enter the year that you would like to test: ")
    try:
        year = int(year)
    except TypeError:
        print("Invalid Input")
        return

    proccessQueue = []

    # Loop through all the days in that year
    date = dt.datetime(year, 1, 1)
    while date.year == year:
        # Im not sure if this is actually any faster than just running it normally
        # Will need to test it
        proccessQueue.append(mp.Process(target = RunSimulation, args=(date, "09d", False)))
        proccessQueue[-1].start()
        date += dt.timedelta(days=1)

    for proccess in proccessQueue:
        proccess.join()

def TestDataSetDates():
    # Get the year that the user wants to be tested
    year = input("Enter the year that you would like to test: ")
    try:
        year = int(year)
    except TypeError:
        print("Invalid Input")
        return
    
    userInput = input("Show events? This may be significantly slower: y/n\n")
    if userInput.lower() == "y":
        showEvents = True
    elif userInput.lower() == "n":
        showEvents = False
    else:
        print("Invalid Input, must be y or n")
        return


    # Load in the file
    with open("DateDataSet.json", "r") as f:
        dataSet = json.load(f)
    
    if not dataSet:
        return

    # Loop through each date changing the year to the desired year
    print("Starting Tests")
    for date in dataSet["dates"]:
        dateTime = dt.datetime.fromisoformat(date)
        dateTime.year = year

        RunSimulation(date, "09d", showEvents)

    print("Tests Complete")



def TestCustomDate():
    # Get the users desired date
    date = input("Enter the date that you would like to test in the format yyyy-mm-dd:\n")

    try:
        dateTime = dt.datetime.fromisoformat(date.replace(" ", ""))
    except:
        print("ERROR: Could not convert to datetime object")
        return
    
    userInput = input("Show events? This may be significantly slower: y/n\n")
    if userInput.lower() == "y":
        showEvents = True
    elif userInput.lower() == "n":
        showEvents = False
    else:
        print("Invalid Input, must be y or n")
        return

    # Run the simulation
    RunSimulation(dateTime, "09d", showEvents)


def TestAllWeather():
    # Loop through all the weather inputs
    for weather in WEATHER_TYPES:
        RunSimulation(dt.datetime.today(), weather, False)

def TestCustomWeather():
    # Get the desired weather from the user
    message = """
    What weather do you want to display:
    1 - Sunny
    2 - Partial Sun
    3 - Slightly Cloudy
    4 - Cloudy
    5 - Rainy
    6 - Partial Sun and Rain
    7 - Stormy
    8 - Snowy
    9 - Foggy
    """

    response = input(message)

    try:
        weather = WEATHER_TYPES[int(response)]
    except:
        print("Invalid Input, must be 1,2,3,4,5,6,7,8 or 9")
        return

    # Run the simulation
    RunSimulation(dt.datetime.today(), weather, False)


def RunSimulation(date:dt.datetime, weather:str, showEvents:bool):
    sys.path.append(os.path.join(PARENT_DIR, "Files"))

    # These will import as i have added the /Files folder to path
    # However IntelliSense doesn't like it
    import RedChannel as red # type: ignore
    import BlackChannel as black # type: ignore
    import FetchApiData as APIs # type: ignore
    
    if weather == None:
        # Fetch New weather data
        weather = APIs.GetWeather()

    events = ""
    if showEvents:
        # get the google calendar events
        events = APIs.GetCalendar(date)

    print(f"Drawing: {date.year}-{date.month}-{date.day} | {weather} | {'Events' if showEvents else 'no Events'}")

    # Draw the image
    red.DATE = date
    red.Draw(weather, events)
    red.image.save(os.path.join("Channels", "RedChannel.png"))

    black.DATE = date
    black.Draw(weather)
    black.image.save(os.path.join("Channels", "BlackChannel.png"))

    # Combine the images into one
    result = sim.Simulate(red.image, black.image)
    # Save it to disk
    result.save(os.path.join("Output", f"{date.year}-{date.month}-{date.day}_{weather}{'_noEvents'if not showEvents else ''}.png"))

if __name__ == "__main__":
    testType = input("What would you like to test:\n1 - Dates\n2 - Weather\n3 - Events\n")
    match(testType):
        case "1":
            dateTestType = input("What dates would you like to test:\n1 - All this year\n2 - Data set (DateDataSet.json)\n3 - Custom\n")
            match(dateTestType):
                case "1":
                    TestAllDates()
                case "2":
                    TestDataSetDates()
                case "3":
                    TestCustomDate()
                case _:
                    print("Invalid Input, must be 1, 2 or 3")

        case "2":
            weatherTestType = input("What weather would you like to test:\n1 - All\n2 - Custom\n")
            match(weatherTestType):
                case "1":
                    TestAllWeather()
                case "2":
                    TestCustomWeather()
                case _:
                    print("Invalid Input, must be 1 or 2")

        case "3":
            eventTest = input("Add Events to the google calendar.\nThen type in 'test' to run the test\n")
            if eventTest.lower() == "test":
                # Run the simulation normally but with a user provided date
                TestCustomDate()
            else:
                print("USER DECLINED - Did not run the test")

        case "0": 
            date = dt.datetime.fromisoformat("2018-01-01")
            RunSimulation(date, "09d", True)


        case _:
            print("Invalid Input, must be 1, 2 or 3")