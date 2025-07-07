"""

Main File

"""


from PIL import Image,ImageDraw,ImageFont
from datetime import date, datetime, timedelta, timezone
import calendar as cal
from googleCalendarAPI import * 
import logging
#Custom files
from MultiLineText import splitText
from GetForcastWeather import Forcast
import Simulate

#E-ink display Library
#from waveshare_epd import epd7in5b_V2
#epd = epd7in5b_V2.EPD()

class EinkCalendar():
    def __init__(self, testDay = -1):
        #Define all the variables needed from the start
        #self.width = epd.width
        #self.height = epd.height

        self.testDay = testDay

        self.forcast = Forcast()
        self.width = 800
        self.height = 480
        self.font5 = ImageFont.truetype("FreeSans.ttf", 10)
        self.font24 = ImageFont.truetype("FreeSans.ttf", 24)
        self.font30 = ImageFont.truetype("FreeSans.ttf", 30)
        self.font36 = ImageFont.truetype("FreeSans.ttf", 36)
        self.allDays = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] #Days of the week
        self.allMonths = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"] #Months of the year
        self.border = 30 #Gap in pixels from edge of image
        self.dataSize = (self.width//3 - self.border, self.height - self.border*2)  # size of the data-Box
        self.calendarSize = ((self.width - self.border) - (self.width//3 + self.border), self.height - self.border*3) #Size of the Calendar
        self.squaresize = (self.calendarSize[0]//7 - 5, self.calendarSize[1]//6 - 5) # size of each day in the Calendar
        self.redOnlyIcons = ["01", "02", "03", "13", "50"]

    #Runs all the Functions for the image to be produced and displayed
    def run(self):
        self.defVars()
        logging.info("Clearing Display")
        self.clear()
        self.getData()
        logging.info("Generating Image")
        self.displayCalendar()
        self.displayData()
        logging.info("Displaying Image")
        self.displayImage()

    def defVars(self):
        self.blackImg = Image.new("1", (800, 480), 255)
        self.blackImg_draw = ImageDraw.Draw(self.blackImg)
        
        self.redImg = Image.new("1", (800, 480), 255)
        self.redImg_draw = ImageDraw.Draw(self.redImg)

        
        if self.testDay == -1:
            self.date = datetime.now(timezone.utc)
            #self.date = datetime(2024, 6, 28, 12, 0, 0, tzinfo=timezone.utc)
        else: 
            self.date = self.testDay

        #define the goolge calendar Class
        self.gooCal = GoogleCalendar()

        #add the calendars from the calendars.json file
        with open(f"{directory}calendars.json", "r") as f:
            jsonText = f.readlines()
            jsonData = json.loads("".join(txt))
            if not jsonData:
                logging.error("No calendars found in calendars.json")
                exit(1)
            for calendar in jsonData["calendars"]:
                logging.log(f"Adding calendar: {calendar['name']}")
                cal.addCalendar(calendar["id"])

        self.month = cal.Calendar().monthdatescalendar(self.date.year, self.date.month)

    #Gets data from the APIs
    def getData(self):

        self.redWeather = 0
        self.blackWeather = 0

        #get the event from google calendar from the start of the month to today + 30 days
        self.events = self.gooCal.Events.getWithin(datetime(self.date.year, self.date.month, 1), self.date + timedelta(days=cal.monthrange(self.date.year, self.date.month)[1]))
        print(self.events)

        if self.testDay != -1:
            logging.info("skipping data fetch")
            self.redWeather = Image.open("Assets/Weather/09d@4xR.png")
            self.blackWeather = Image.open("Assets/Weather/09d@4xB.png")
            self.isWeather = True
            return
        
        logging.info("getting Data")

        forcastdata = self.forcast.getForcast()
        icon = forcastdata[2]
        if not icon:
            self.isWeather = False
            return
        else: self.isWeather = True
        
        self.redWeather = Image.open(f"Assets/Weather/{icon[:-1]}d@4xR.png")
        if icon[:-1] in self.redOnlyIcons:
            self.blackWeather = None
        else:
            self.blackWeather = Image.open(f"Assets/Weather/{icon[:-1]}d@4xB.png")
       
    #Right hand side of the calendar... shows this month
    def displayCalendar(self):
        #Calendar
        #loops + counters
        todayIsDone = False
        counter = 0
        lastCount = 0
        for weeks in range(0, 6):
            for day in range(0, 7):
                try:
                    #if it is of current month add 1
                    if self.month[weeks][day].month == self.date.month:
                        counter += 1
                        boxfill = 255 # red/black
                    else:
                        boxfill = 0 # white
                except IndexError:
                    boxfill = 0 #white

                #calculates the top left of the square for each box
                topleft = (self.width//3 + self.border + self.calendarSize[0]//7 * day, self.border * 2 + self.calendarSize[1]//6 * weeks)
                
                #If first row: write days of the week
                if weeks == 0:
                    self.blackImg_draw.text((topleft[0] + self.squaresize[0]//2, self.border * 1.4), self.allDays[day], font = self.font24, fill = 0, anchor= "mm")
                
                #Make today highlighted in red
                if self.date.day == counter and not todayIsDone:
                    textfill = 255
                    
                    # Red Calendar
                    self.redImg_draw.rectangle((topleft[0], topleft[1], topleft[0] + self.calendarSize[0]//7 - 5, topleft[1] + self.calendarSize[1]//6 - 5), fill = 0)
                    self.redImg_draw.text((topleft[0] + self.squaresize[0]//2, topleft[1] + self.squaresize[1]//2), f"{counter}", font=self.font36, fill= 255, anchor = "mm")
                    todayIsDone = True # fixes issue where at the end of the month the rest of the remaining boxes will be that day and red
                else:
                    textfill = 0
                
                # black Calendar
                #Draw all the boxes on the calendar
                self.blackImg_draw.rectangle((topleft[0], topleft[1], topleft[0] + self.calendarSize[0]//7 - 5, topleft[1] + self.calendarSize[1]//6 - 5), outline = 0, width=3, fill = boxfill)
                self.blackImg_draw.text((topleft[0] + self.squaresize[0]//2, topleft[1] + self.squaresize[1]//2), f"{counter}", font= self.font36, fill= textfill, anchor="mm")

                #draw a little red box if there is an event on that day
                if counter <= 0 or counter == lastCount: continue
                
                #If there is a event on that day
                if len(self.gooCal.Events.isEvent(datetime(self.date.year, self.date.month, 1, tzinfo=timezone.utc) + timedelta(days=counter-1))) > 0:
                    #draw red box                        X           Y                   X            Y
                    self.redImg_draw.rectangle((topleft[0] + 4, topleft[1] + 4, topleft[0] + 12, topleft[1] + 12), outline = 0, width= 8, fill = boxfill)

                lastCount = counter

    #all data that is shown... day, weather, month, year, calendar events... may add more
    def displayData(self):
        #add the time at the to
        self.blackImg_draw.text((750, 10), f"{self.date.hour}:{self.date.minute}:{self.date.second}", font=self.font5, fill=0, anchor="mm")

        #Draw box where data is going to be shown
        self.redImg_draw.rectangle((self.border, self.border, self.dataSize[0] + self.border, self.dataSize[1] + self.border), fill= 0)

        #define date suffix
        todayDay = int(str(self.date.day)[-1]) - 1
        suffixList = ["st", "nd", "th"]
        if todayDay > 2: todayDay = 2
        suffix = suffixList[todayDay]

        #Add the Date and underline it
        dataMiddle = self.border + self.dataSize[0]//2
        dt = f"{self.date.day}{suffix} {self.allMonths[self.date.month-1]} {self.date.year}"
        self.redImg_draw.text((dataMiddle, self.border * 2), dt, fill = 255, font=self.font30, anchor="mm")
        self.redImg_draw.line((self.border * 1.5, self.border * 2.75, self.dataSize[0] + self.border * 0.5, self.border * 2.75), fill = 255, width =3)

        #add todays holiday events
        todayEvents = self.gooCal.Events.isEvent(self.date)
        if len(todayEvents) > 0:
            text = ""
            for item in todayEvents:
                text += f"{item[1]['summary']} \n"
            textArray = (splitText(text, 20)).split(" \n")
            try:
                textArray.remove(" ")
            except ValueError: pass
            
            for index, item in enumerate(textArray):
                item = item.replace("\n", "")
                self.redImg_draw.text((dataMiddle, (self.border * 3.5) + (index * self.border)), item, fill = 255, anchor="mm", font = self.font24)


        #Add Weather icon2
        if not self.isWeather: return
        self.redImg.paste(self.redWeather, ((self.border*3)//2+self.border//10, self.height-self.border*8))
        if self.blackWeather:
            self.blackImg.paste(self.blackWeather, ((self.border*3)//2+self.border//10, self.height-self.border*8))

        #show next event
        nextEvent = self.gooCal.Events.next(self.date)
        #logging.debug(str(nextEvent))
        if nextEvent != None:
            #text saying 'next event: ____'
            self.redImg_draw.text((dataMiddle, (self.border * 8.5)), f"Next Event:\n{splitText(self.gooCal.Events.next(self.date)['summary'], 20)}", fill = 255, anchor="mm", font = self.font24)
            pass
            

    def displayImage(self):
        self.blackImg = self.blackImg.transpose(Image.ROTATE_180)
        self.redImg = self.redImg.transpose(Image.ROTATE_180)
        self.blackImg.save("OutputImgs/blckImg.png")
        self.redImg.save("OutputImgs/redImg.png")
        #display the image to the e-ink display


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s  |  %(levelname)s : %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)
    logging.debug("Starting")
    Cal = EinkCalendar()
    Cal.run()
    img = Simulate.start()
    img.save("OutputImgs/output.png")
    logging.debug("Complete")
    img.show()

