# Simulate.py
# This file simulates how it would be displayed on the e-ink display without having to put it on the display
# Author: Marlon Otter
# Date (dd-mm-yyy): 10-07-2025


from PIL import Image

def Start():
    red = Image.open("Output/red_channel.png")
    black = Image.open("Output/black_channel.png")
    img = Simulate(red, black)
    return img

def Simulate(rImg, bImg):
    rImg = convert(rImg)
    bImg = convert(bImg)
    redpixelImg = rImg.load()
    for x in range(rImg.size[0]):
        for y in range(rImg.size[1]):
            if redpixelImg[x, y] == (255, 255, 255, 255):
                redpixelImg[x, y] = (0, 0, 0, 0)
            elif redpixelImg[x, y] == (0, 0, 0, 255):
                redpixelImg[x, y] = (170, 41, 41, 255)
    bImg.paste(rImg, (0, 0), rImg)
    return bImg

def convert(img):
    new = Image.new(size = img.size, mode="RGBA")
    pixelNew = new.load()
    pixelImg = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if pixelImg[x, y] == 255:
                pixelNew[x, y] = (255, 255, 255, 255)
            elif pixelImg[x, y] == 0:
                pixelNew[x, y] = (0, 0, 0, 255)
    return new        
    


if __name__ == "__main__": 
    img = Start()  
    img.show()