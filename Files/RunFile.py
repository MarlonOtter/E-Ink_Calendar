import controlDisplay
from datetime import datetime
import logging
import sys
sys.path.append("/home/raspberry/Documents/E-Ink-Calendar-main")

#logging.basicConfig(filename = "Calendarlog.log", format='%(asctime)s | %(levelname)s : %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)#

lastRan = -1
cTime = datetime.now().time()
if cTime.hour != lastRan:
    lastRan = cTime.hour
    logging.info("-- Running Program --")
    controlDisplay.run()
    logging.debug(f"Waiting -> lastRan : {lastRan} ----------------")
    
# 0 */3 * * * python3 /home/raspberry/Documents/E-Ink-Calendar-main/RunFile.py

