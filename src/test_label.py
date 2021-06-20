import requests
import subprocess
import os
import json
import sys

def readLabelFile(labelNumber):
    with open('/labels/' + labelNumber + '.txt', 'rt') as labelFile:
        labelName = labelFile.readline()
        return labelName.strip()

def readConfigFile():
    with open('/config/printerbox_config.json') as config_file:
        config = json.load(config_file)
        return config

def printFile(fileName, labelName):
    print("Printing: " + fileName)
    media = 'media=' + labelName
    printCmd = ['lp', '-d', 'TD4550DNWB', '-h', 'printerbox_sortkaffe_cupsd_1', '-o', media, '-o', 'BrTrimtape=OFF', fileName]
    #print(printCmd)
    output = subprocess.run(printCmd, capture_output=False)
    return output.returncode


#### Main

if(len(sys.argv) != 1):
    print("Please provide label as argument")

labelNumber = sys.argv[0]

print("Printing test label " + labelNuber)

config_file = readConfigFile()
boxId = config_file['config']['boxid']

print("PrinterBox: " + boxId)

labelName = readLabelFile(labelNumber)
print("LabelType: " + labelNumber)

nameTagPdf = "test_labels/test_label_" + labelNumber + ".pdf"

if(printFile(nameTagFileName, labelName) == 0):
    blinkGreen()

