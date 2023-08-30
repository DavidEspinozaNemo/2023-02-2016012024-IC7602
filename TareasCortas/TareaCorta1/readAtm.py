initSection = "InitSection"
endSection = "EndSection"
fileExtension = ".atm"
elementDivision = "\n"

audio = []
fourierAudio = []

#Puedo mezclar los dos datos para solo hacer un recorrido. Asumiendo que ambos arrays son del mismo tamano.

def guardarArchivo(audioArray,fourierAudioArray,path,fileName):
    fileData = ""
    #Audio section in file
    fileData += initSection+elementDivision
    for element in audioArray:
        fileData += element+elementDivision
    fileData += endSection+elementDivision
    #Fourier section in file
    fileData += initSection+elementDivision
    for element in fourierAudioArray:
        fileData += element+elementDivision
    fileData += endSection+elementDivision

    with open(path+fileName+fileExtension, 'r') as file:
        file.write(fileData)
        file.close()

    
def processFileLines(lines):
    dataSections = []
    isSection = False
    for line in lines:
        line = line.replace(elementDivision,"")
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