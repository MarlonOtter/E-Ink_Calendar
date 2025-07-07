from PIL import Image

def start():
    red = Image.open("OutputImgs/redImg.png")
    black = Image.open("OutputImgs/blckImg.png")
    img = sim(red, black)
    return img

def sim(rImg, bImg):
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
    img = start()  
    img.show()