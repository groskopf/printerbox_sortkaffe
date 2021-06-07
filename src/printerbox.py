import requests
import subprocess
import os
import json
import time
import datetime

printInfoUrl      = 'https://app.conferencecommunicator.com/plugins/printbox/GetPrintBoxinfo.vbhtml?BoxID='
printQueuePdfUrl    = 'https://app.conferencecommunicator.com/UserData/PrintQueue/PDF/'
printGetQueueUrl    = 'https://app.conferencecommunicator.com/plugins/printbox/GetPrintBoxQueue.vbhtml?BoxID='
printUpdateQueueUrl = 'https://app.conferencecommunicator.com/plugins/printbox/UpdatePrintBoxQueue.vbhtml?ID='


def blinkOff():
    blinkCmd = ['blink1-tool', '--off', '/dev/null']
    output = subprocess.run(blinkCmd, capture_output=True)
    return output.returncode  

def blinkWhite():
    blinkCmd = ['blink1-tool', '--white', '--blink=1', '/dev/null']
    output = subprocess.run(blinkCmd, capture_output=True)
    return output.returncode  

def blinkGreen():
    blinkCmd = ['blink1-tool', '--green', '--blink=1', '/dev/null']
    output = subprocess.run(blinkCmd, capture_output=True)
    return output.returncode  

def getLabelNumber(boxId):
    printInfo = requests.get(printInfoUrl + boxId)
    printInfoList = printInfo.text.split('$$')
    return printInfoList[0]

def readLabelFile(labelNumber):
    with open('/labels/' + labelNumber + '.txt', 'rt') as labelFile:
        labelName = labelFile.readline()
        return labelName.strip()

def readConfigFile():
    with open('/config/printerbox_config.json') as config_file:
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
    printCmd = ['lp', '-d', 'TD4550DNWB', '-h', 'printerbox_sortkaffe_cupsd_1', '-o', media, '-o', 'BrTrimtape=OFF', fileName]
    #print(printCmd)
    output = subprocess.run(printCmd, capture_output=False)
    return output.returncode

def updatePrintQueue(boxId):
    output = requests.post(printUpdateQueueUrl + boxId)
    return output.status_code


#### Main

blinkOff()

print("Starting Attendwise PrinterBox")

config_file = readConfigFile()
boxId = config_file['config']['boxid']

print("PrinterBox: " + boxId)

labelNumber = getLabelNumber(boxId)
labelName = readLabelFile(labelNumber)
print("LabelType: " + labelNumber)

lastPrintTime = datetime.datetime.now()

while True:

    minutesSinceLastPrint = (datetime.datetime.now() - lastPrintTime).total_seconds()
    if(minutesSinceLastPrint > 10 * 60):
    	time.sleep(4)
    else:
    	time.sleep(1)
    
    printQueueList = getPrintQueue(boxId)

    blinkWhite()

    #print("Retreiving list:")
    #print(printQueueList)
        
    for printQueueElement in printQueueList:
        if(not printQueueElement):
            continue

        printElementAttributes = printQueueElement.split(',')
        nameTagFileName = printElementAttributes[0]
   
        nameTagPdf = downloadPdfFile(nameTagFileName)

        savePdfFile(nameTagFileName, nameTagPdf.content)

        lastPrintTime = datetime.datetime.now()

        if(printFile(nameTagFileName, labelName) == 0):
            blinkGreen()
            os.remove(nameTagFileName)
            updatePrintQueue(nameTagFileName)

