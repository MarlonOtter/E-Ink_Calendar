from Calendar import *

#E-ink display Library
from waveshare_epd import epd7in5b_V2
epd = epd7in5b_V2.EPD()

def run():
    try:
        logging.info("Starting")
        #Generate images
        cal = EinkCalendar()
        cal.run()
        #get Images
        red = Image.open("OutputImgs/redImg.png")
        black = Image.open("OutputImgs/blckImg.png")
        logging.info("Image Generated")
        #Clear Display
        logging.info("Clearing Display")
        epd.init()
        epd.Clear()
        logging.info("Cleared")
        #Display Image
        logging.info("Displaying Image")
        epd.display(epd.getbuffer(black), epd.getbuffer(red))
        logging.info("Image Displayed")
        epd.sleep()
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd7in5_V2.epdconfig.module_exit()
        exit()
    logging.info("DONE - Sleeping")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s  |  %(levelname)s : %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)
    run()
    #input("Press ENTER to close: ")
