from Calendar import *



if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s  |  %(levelname)s : %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.DEBUG)

    day = datetime(2024, 1, 1)

    for i in range(366):
        logging.debug(f"Starting: {i}")
        Cal = EinkCalendar(testDay=day)
        Cal.run()
        img = Simulate.start()
        img.save(f"OutputImgs/output-{i}.png")
        logging.debug(f"Complete: {i}")

        day += timedelta(days=1)