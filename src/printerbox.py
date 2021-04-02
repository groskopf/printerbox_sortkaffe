import requests
import subprocess
import os
import json

printQueuePdfUrl = 'https://app.conferencecommunicator.com/UserData/PrintQueue/PDF/'
printQueueUrl = 'https://app.conferencecommunicator.com/plugins/printbox/GetPrintBoxQueue.vbhtml?BoxID='


def readLabelFile():
    with open('/labels/navneskilt.txt', 'rt') as navneskilt:
        labelName = navneskilt.readline()
        return labelName.strip()

def readConfigFile():
    with open('/src/printerbox_config.json') as config_file:
        config = json.load(config_file)
        return config

def savePdfFile(fileName, content):
    file = open(fileName, "wb")
    file.write(content)
    file.close()

def downloadPdfFile(fileName):
    nameTagUrl = printQueuePdfUrl + fileName
    nameTagPdf = requests.get(nameTagUrl)
    return nameTagPdf

def getPrintQueue(boxId):
    printQueue = requests.get(printQueueUrl + boxId)
    printQueueList = printQueue.text.split('$$')
    return printQueueList

def printFile(fileName, labelName):
    print(fileName)
    media = 'media=' + labelName
    printCmd = ['lp', '-d', 'TD4550DNWB', '-h', 'cupsd', '-o', media, fileName]
    print(printCmd)
    output = subprocess.run(printCmd, capture_output=False)
    output = subprocess.run(['ls', fileName], capture_output=False)
    return output.returncode

def dequeueFile(fileName):
    output = subprocess.run(["ls", fileName], capture_output=True)
    return output.returncode


#### Main

config_file = readConfigFile();
boxid = config_file['config']['boxid']

labelName = readLabelFile()


printQueueList = getPrintQueue(boxid)

print("Hello world")
print(printQueueList )

for printQueueElement in printQueueList:
    if(not printQueueElement):
        continue

    printElementAttributes = printQueueElement.split(',')
    nameTagFileName = printElementAttributes[0]
   
    nameTagPdf = downloadPdfFile(nameTagFileName)

    savePdfFile(nameTagFileName, nameTagPdf.content)

    printFile(nameTagFileName, labelName)
    #if(printFile(nameTagFileName) == 0):
     #   os.remove(nameTagFileName)
      #  dequeueFile(nameTagFileName)

