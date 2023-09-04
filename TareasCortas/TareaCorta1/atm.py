import json
import shutil
import os
import zipfile

folderPathATM = "TareasCortas/TareaCorta1/ATMFiles"
folderPathWAV = "TareasCortas/TareaCorta1/WavFiles"
audioFormat = ".wav"
fileFormat = ".atm"
compressionFormat = "zip"
jsonFileName = 'data.json'

#Tirar excepcion si no se carga bien
def save(audioData,fourierData,audioFrecuency,audioFileName):

    #Create new folder
    atmPath = folderPathATM+"/"+audioFileName
    if os.path.exists(atmPath):
        shutil.rmtree(atmPath, ignore_errors=True)
    os.makedirs(atmPath)

    #Move audio to new path
    shutil.move(folderPathWAV+"/"+audioFileName+audioFormat, atmPath)

    #Save audio data in a json
    data = {
        "audioData" : audioData,
        "fourierData" : fourierData,
        "audioFrecuency" : audioFrecuency
    }
    with open(atmPath+'/'+jsonFileName, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    #Create zip file and add atm extension
    shutil.make_archive(atmPath,compressionFormat,atmPath)
    os.rename(atmPath+"."+compressionFormat, atmPath+fileFormat)
    if os.path.exists(atmPath):
        shutil.rmtree(atmPath, ignore_errors=True)
    print(f"Created {fileFormat} file: {atmPath}{fileFormat}")

def load(audioFileName):
    #Change name to zip to unzip file.
    atmPath = folderPathATM+"/"+audioFileName
    zipPath = atmPath+"."+compressionFormat
    os.rename(atmPath+fileFormat , zipPath)

    #Open zip file and json file
    with zipfile.ZipFile(zipPath, "r") as file:
        with file.open(jsonFileName) as jsonFile:  
            utf = jsonFile.read()  
            data = json.loads(utf) 
    
    os.rename(zipPath,atmPath+fileFormat)
    print(f"Loaded {fileFormat} file: {atmPath}{fileFormat}\n data: {data}")
    return data

#Save para crear un nuevo archivo.
#save("xd","lmao",60,"ElTest2")
#Load para cargar un archivo existente.
#load("ElTest2")