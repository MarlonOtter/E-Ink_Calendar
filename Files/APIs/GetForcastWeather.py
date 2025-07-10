# GetForcastWeather.py
# Gets the Weather Forcast for today 
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025


from datetime import datetime
import requests as req
import json
from dateutil import parser
import os 

class Forcast():
    def __init__(self):
        
        # read the file storing all sensative information
        with open(os.path.join(os.path.dirname(__file__), "secrets", "OpenWeatherMap", "key.json"), "r") as f:
            APIinfo = json.load(f)

        # Generate a url that will be used to make a request to
        self.url = f"https://api.openweathermap.org/data/2.5/forecast?lat={APIinfo['lat']}&lon={APIinfo['lon']}&units=metric&appid={APIinfo['key']}" #final url
    
    def getForcast(self):
        cDateTime = datetime.now()
        self.cTime = datetime(cDateTime.year, cDateTime.month, cDateTime.day, 21)

        self.fetchData()
        self.handleData()
        return self.returnData()

    def fetchData(self):
        self.reqData = req.get(self.url).json()

    def handleData(self):
        #get the weather for today and time
        #loop through all the data finding selecting the one with current data + time
        for item in self.reqData["list"]:
            itemTime = parser.parse(item["dt_txt"])
            if itemTime == self.cTime:
                #Returns weather and temperature Data
                self.weather = item["weather"][0]["main"]
                self.temp = round(item["main"]["temp"])
                break
        else:
            self.weather, self.temp = None, None
        
        if self.weather:
            self.icon = item["weather"][0]["icon"]
        else:
            self.icon = None

    def returnData(self):
        #returns data to main function
        data = [self.weather, self.temp, self.icon]
        return data


#Only ran if this file is ran directly
if __name__ == "__main__":
    
    #Defines class
    app = Forcast()

    #Calls main function
    forcastData = app.getForcast()
    
    #outputs returned data
    print(forcastData)

