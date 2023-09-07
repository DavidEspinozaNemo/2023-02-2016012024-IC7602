import json
import shutil
import os
import zipfile

#folderPathATM = "TareasCortas/TareaCorta1/ATMFiles"
fileFormat = ".atm"
compressionFormat = "zip"
jsonFileName = 'dataATM.json'

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
    shutil.move(audioSourcePath+"/"+audioFileName, atmPath)

    with open(atmPath+'/'+jsonFileName, 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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
        with file.open(jsonFileName) as jsonFile:  
            utf = jsonFile.read()  
            data = json.loads(utf) 
    
    os.rename(zipPath,filePath)
    print(f"Loaded {fileFormat} file: {filePath}\n data: {data}")
    return data

#Save para crear un nuevo archivo.
#save("xd","lmao",60,"ElTest2")
#Load para cargar un archivo existente.
#load("ElTest2")