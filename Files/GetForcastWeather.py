#import time
from datetime import date, datetime
import requests as req
import json
from dateutil import parser
from PIL import Image
from io import BytesIO

# CHANGE : Might make it so new data is requested every day instead of every 5 days
#        :

class Forcast():
    def __init__(self):
        #Defines all variables that do not change
        #Create url for api
        lat, lon = 53.388, -1.496 #Location                                                                                       
        apiKey = "c8ece20034d425412af71ca46473ff84" #Key for api account
        self.url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={apiKey}" #final url
    
    def getForcast(self):
        #main Function
        #calls all other Functions and returns data
        self.defVars()
        self.fetchData()
        self.handleData()
        return self.returnData()

    def defVars(self):
        #defines all variables that change
        cDateTime = datetime.now()
        self.cTime = datetime(cDateTime.year, cDateTime.month, cDateTime.day, 21)
        #print(self.cTime)

    def fetchData(self):
        #Check if new data is needed
        #reads final data item in WeatherData.json file and checks if that is before the currnet date and time
        # if so it will request new data
        with open("WeatherData.json", "r") as rf:
            #print("reading Data")
            jsonData = json.load(rf)
            dtStr = jsonData["list"][-1]["dt_txt"]
            dtObject = parser.parse(dtStr)
        tSpan = dtObject - self.cTime
        if tSpan.days > 0:
            self.reqData = jsonData
        else:
            #Get New data
            #Writes data recieved from website to a file called WeatherData.json
            print("requesting New Data")
            self.reqData = req.get(self.url).json()
            with open("WeatherData.json", "w") as wf:
                json.dump(self.reqData, wf, indent= 4)
            #print("Saved New Data")

    def handleData(self):
        #get the weather for today and time
        #loop through all the data finding selecting the one with current data + time
        for item in self.reqData["list"]:
            itemTime = parser.parse(item["dt_txt"])
            if itemTime == self.cTime:
                #Returns weather and temperature Data
                #print("Date and time FOUND")
                self.weather = item["weather"][0]["main"]
                self.temp = round(item["main"]["temp"])
                break
        else:
            self.weather, self.temp = None, None
            #print("Data NOT found for this hour")
        
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

