# MultiLineText.py
# Splits up multiple lines of text grouping words together
# Author: Marlon Otter
# Date (dd-mm-yyy): xx-xx-2022

def splitText(inputStr, lineLength):
    if len(inputStr) <= lineLength:
        return inputStr
    
    #separate each word into an array
    splitStr = inputStr.split(" ")
    total = 0
    splitlinePos = []
    for index, item in enumerate(splitStr):
        total += len(item) + 1
        if total > lineLength:
            splitlinePos.append(index)
            total = len(item)
    for item in splitlinePos:
        for index, word in enumerate(splitStr):
            if index == item:
                splitStr[index] = f"\n{word}"
                
    outputStr = ""
    for item in splitStr:
        outputStr += item + " "
    return outputStr



if __name__ == "__main__":
    # Just some randomly generated sentence
    string = "Truth in advertising and dinosaurs with skateboards have much in common. David subscribes to the 'stuff your tent into the bag' strategy over nicely folding it."
    text = splitText(string, 10)
    print(text)



