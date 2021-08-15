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

def blinkRed(n = 1):
    blinkCmd = ['blink1-tool', '--red', '--blink=' + str(n), '/dev/null']
    output = subprocess.run(blinkCmd, capture_output=True)
    return output.returncode  

def blinkGreen(n = 1):
    blinkCmd = ['blink1-tool', '--green', '--blink=' + str(n), '/dev/null']
    output = subprocess.run(blinkCmd, capture_output=True)
    return output.returncode  

def blinkBlue(n = 1):
    blinkCmd = ['blink1-tool', '--blue', '--blink=' + str(n), '/dev/null']
    output = subprocess.run(blinkCmd, capture_output=True)
    return output.returncode  

def blinkMagenta(n = 1):
    blinkCmd = ['blink1-tool', '--magenta', '--blink=' + str(n), '/dev/null']
    output = subprocess.run(blinkCmd, capture_output=True)
    return output.returncode  

def getLabelNumber(boxId):
    try:
        url = printInfoUrl + boxId
        r = requests.get(url)
        r.raise_for_status()
        printInfoList = r.text.split('$$')
        return printInfoList[0]
    except requests.exceptions.HTTPError as errh:
        print (url + "Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print (url + "Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print (url + "Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print (url + "OOps: Something Else",err)
    return None


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
    try:
        url = printQueuePdfUrl + fileName
        nameTagPdf = requests.get(url)
        nameTagPdf.raise_for_status()
        return nameTagPdf
    except requests.exceptions.HTTPError as errh:
        print (url + "Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print (url + "Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print (url + "Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print (url + "OOps: Something Else",err)
    return None

def getPrintQueue(boxId):
    try:
        url = printGetQueueUrl + boxId
        printQueue = requests.get(url)
        printQueueList = printQueue.text.split('$$')
        return printQueueList
    except requests.exceptions.HTTPError as errh:
        print (url + "Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print (url + "Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print (url + "Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print (url + "OOps: Something Else",err)
    return None

def printFile(fileName, labelName):
    print("Printing: " + fileName)
    media = 'media=' + labelName
    printCmd = ['lp', '-d', 'TD4550DNWB', '-h', 'printerbox_sortkaffe_cupsd_1', '-o', media, '-o', 'BrTrimtape=OFF', fileName]
    print(printCmd)
    output = subprocess.run(printCmd, capture_output=False)
    return output.returncode

def updatePrintQueue(boxId):
    try:
        url = printUpdateQueueUrl + boxId
        output = requests.post(printUpdateQueueUrl + boxId)
        output.raise_for_status()
        return
    except requests.exceptions.HTTPError as errh:
        print (url + "Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print (url + "Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print (url + "Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print (url + "OOps: Something Else",err)
    blinkRed(5)
    time.sleep(4)
    

#### Main

blinkOff()

print("Starting Attendwise PrinterBox")

config_file = readConfigFile()
boxId = config_file['config']['boxid']

print("PrinterBox: " + boxId)

labelNumber = getLabelNumber(boxId)
while not labelNumber:
    blinkRed(2)
    time.sleep(4)
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
    
    blinkGreen()
    printQueueList = getPrintQueue(boxId)
    if not printQueueList:
        blinkRed(3)
        time.sleep(4)
        continue
        
    for printQueueElement in printQueueList:
        if(not printQueueElement):
            continue

        print("Retreiving list:")
        print(printQueueList)

        printElementAttributes = printQueueElement.split(',')
        nameTagFileName = printElementAttributes[0]
   
        nameTagPdf = downloadPdfFile(nameTagFileName)
        if not nameTagPdf:
            updatePrintQueue(nameTagFileName)
            blinkRed(4)
            time.sleep(4)
            continue

        savePdfFile(nameTagFileName, nameTagPdf.content)

        lastPrintTime = datetime.datetime.now()

        if(printFile(nameTagFileName, labelName) == 0):
            blinkBlue()
            os.remove(nameTagFileName)
            updatePrintQueue(nameTagFileName)
        else:
            blinkMagenta()

