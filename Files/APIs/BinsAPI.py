#
# NOTE : This will likely only work for my location so will not be required to run the program to work still
#

import os
import json

import requests
from bs4 import BeautifulSoup as bs
import datetime as dt

APIinfo = {}

secretsPath = os.path.join(os.path.dirname(__file__), "secrets", "bins.json") 

if (os.path.isfile(secretsPath)):
    with open(secretsPath, "r") as f:
        APIinfo:json = json.load(f)
else:
    print("Missing Bins secret: Bins API will not be used")

def getNextBinDates():
    if (not APIinfo):
        return
    
    r = requests.get(APIinfo["HouseURL"])
    soup = bs(r.content, 'html.parser')
    
    next = soup.find_all("td", class_="next-service")
    if (next):
        dates = []
        for group in next:
            dates.append(group.contents[2])
        return Bins(dates)
    return 


class Bins():
    def __init__(self, allDates:list):
        self.black = self.parseDates(allDates[0])
        self.green = self.parseDates(allDates[1])
        self.blue = self.parseDates(allDates[2])
        self.brown = self.parseDates(allDates[3])
        
        
    def parseDates(self, dates:str):
        # recieves: 23 Oct 2025, 6 Nov 2025, 20 Nov 2025
        dates = dates.replace("\t", "").replace("\r", "").replace("\n", "")
        individualDates = dates.split(",")
        dateArr = []
        for dateString in individualDates:
            dateArr.append(dt.datetime.strptime(dateString.strip(), "%d %b %Y"))
        return dateArr
    
    def to_string(self, bin:list, seperator:str=", "):
        string = ""
        for date in bin:
            string += date.strftime("%d %B %Y") + seperator
        return string
    
    def getTomorrow(self, date):
        def getBinTomorrow(bin:list, result:str): 
            for binDate in bin:
                dayBeforeBin = binDate + dt.timedelta(days=-1)
                if dayBeforeBin.date() == date.date():
                    return result 
            
        return (getBinTomorrow(self.black, "black") or
        getBinTomorrow(self.green, "green") or
        getBinTomorrow(self.blue, "blue") or
        getBinTomorrow(self.brown, "brown"))
        
if __name__ == "__main__":
    bins = getNextBinDates()
    print(bins.getTomorrow(dt.datetime.today()))
    if (bins):
        print(f"black: {bins.to_string(bins.black)}\ngreen: {bins.to_string(bins.green)}\nblue: {bins.to_string(bins.blue)}\nbrown: {bins.to_string(bins.brown)}\n")
    else:
        print("NO BIN DATA RECIVED")        
