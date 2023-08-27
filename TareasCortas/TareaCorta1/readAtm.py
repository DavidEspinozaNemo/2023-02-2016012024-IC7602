initSection = "InitSection"
endSection = "EndSection"
lineDivision = "\n"

audio = []
fourierAudio = []
    
def processFileLines(lines):
    dataSections = []
    isSection = False
    for line in lines:
        line = line.replace(lineDivision,"")
        if line == endSection:
            dataSections.append(dataSection)
            isSection = False
        if isSection:
            dataSection.append(line)
        if line == initSection:
            dataSection = []
            isSection = True
    return dataSections

def openATMFile(path):
    with open(path, 'r') as file: #open the file
        return file.readlines() #put the lines to a variable (list).

audio,fourierAudio = processFileLines(openATMFile("ATMFiles/test.atm"))

print(audio)
print(fourierAudio)