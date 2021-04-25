import requests
import subprocess
import os
import json

printQueuePdfUrl =    'https://app.conferencecommunicator.com/UserData/PrintQueue/PDF/'
printGetQueueUrl =       'https://app.conferencecommunicator.com/plugins/printbox/GetPrintBoxQueue.vbhtml?BoxID='
printUpdateQueueUrl = 'https://app.conferencecommunicator.com/plugins/printbox/UpdatePrintBoxQueue.vbhtml?ID='

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
    printQueue = requests.get(printGetQueueUrl + boxId)
    printQueueList = printQueue.text.split('$$')
    return printQueueList

def printFile(fileName, labelName):
    print("Printing: " + fileName)
    media = 'media=' + labelName
    printCmd = ['lp', '-d', 'TD4550DNWB', '-h', 'printerbox_sortkaffe_cupsd_1', '-o', media, fileName]
    #print(printCmd)
    #output = subprocess.run(printCmd, capture_output=False)
    output = subprocess.run(['ls', fileName], capture_output=False)
    return output.returncode

def updatePrintQueue(boxId):
    output = requests.post(printUpdateQueueUrl + boxId)
    return output.status_code


#### Main

print("Starting SortKaffe PrinterBox")

config_file = readConfigFile();
boxid = config_file['config']['boxid']

print("PrinterBox: " + boxid)

# FIXME retrive the label from the server
labelName = readLabelFile()

# FIXME while for ever
printQueueList = getPrintQueue(boxid)

print("Retreiving list:")
print(printQueueList)

for printQueueElement in printQueueList:
    if(not printQueueElement):
        continue

    printElementAttributes = printQueueElement.split(',')
    nameTagFileName = printElementAttributes[0]
   
    nameTagPdf = downloadPdfFile(nameTagFileName)

    savePdfFile(nameTagFileName, nameTagPdf.content)

    if(printFile(nameTagFileName, labelName) == 0):
        os.remove(nameTagFileName)
        updatePrintQueue(nameTagFileName)

