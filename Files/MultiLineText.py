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
    string = "Hello my name is marlon Otter, I am 15 years old and these lines can only be a maximum of 10 characters long"
    #string = "1 2 3 4 5 1 2 3 4 5 1 2 3 4 5"
    text = splitText(string, 10)
    print(text)



