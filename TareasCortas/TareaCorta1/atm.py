import json
import shutil
import os
import tempfile
import wave
import zipfile

import pyaudio

#folderPathATM = "TareasCortas/TareaCorta1/ATMFiles"
fileFormat = ".atm"
compressionFormat = "zip"
jsonFileName = 'data.json'
CHUNK = 1024

'''
DATA EXAMPLE
    #Save audio data in a json
    data = {
        "audioData" : audioData,
        "fourierData" : fourierData,
        "audioFrecuency" : audioFrecuency
    }
'''

#Tirar excepcion si no se carga bien
def save(data,audioSourcePath,ATMSavePath,audioFileName):

    #Create new folder
    atmPath = ATMSavePath+"/"+audioFileName
    if os.path.exists(atmPath):
        shutil.rmtree(atmPath, ignore_errors=True)
    os.makedirs(atmPath)

    #Move audio to new path
    shutil.move(audioSourcePath, atmPath)

    with open(atmPath+'/'+jsonFileName, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        file.close()

    #Create zip file and add atm extension
    shutil.make_archive(atmPath,compressionFormat,atmPath)
    os.rename(atmPath+"."+compressionFormat, atmPath+fileFormat)
    if os.path.exists(atmPath):
        shutil.rmtree(atmPath, ignore_errors=True)
    print(f"Created {fileFormat} file: {atmPath}{fileFormat}")

def load(filePath):
    #Change name to zip to unzip file.
    zipPath = filePath.replace(fileFormat,"."+compressionFormat)
    os.rename(filePath , zipPath)
    #Open zip file and json file
    with zipfile.ZipFile(zipPath, "r") as file:
        nameList = file.namelist()
        nameList.remove(jsonFileName)
        tempWAV = tempfile.NamedTemporaryFile()
        tempWAV.write(file.read(nameList[0]))
        tempWAV.seek(0)

        with file.open(jsonFileName) as jsonFile:  
            utf = jsonFile.read()  
            atmData = json.loads(utf) 
            jsonFile.close()
        file.close()

    os.rename(zipPath,filePath)

    print(f"Loaded {fileFormat} file: {filePath}\n data: {atmData}")

    return atmData,tempWAV

#Save para crear un nuevo archivo.
#save("xd","F:\GitHub\\2023-02-2016012024-IC7602\TareasCortas\TareaCorta1\WavFiles\grabacion.wav","F:\GitHub\\2023-02-2016012024-IC7602\TareasCortas\TareaCorta1\ATMFiles","grabacion")
#Load para cargar un archivo existente.
#load("TareasCortas\TareaCorta1\ATMFiles\grabacion.atm")