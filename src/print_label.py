import requests
import subprocess
import os
import json
import sys

def blinkGreen(n = 1):
    blinkCmd = ['blink1-tool', '--green', '--blink=' + str(n), '/dev/null']
    output = subprocess.run(blinkCmd, capture_output=True)
    return output.returncode

def readLabelFile(labelNumber):
    with open('/labels/' + labelNumber + '.txt', 'rt') as labelFile:
        labelName = labelFile.readline()
        return labelName.strip()

def printFile(fileName, labelName):
    print("Printing: " + fileName)
    media = 'media=' + labelName
    printCmd = ['lp', '-d', 'TD4550DNWB', '-h', 'printerbox_sortkaffe_cupsd_1', '-o', media, '-o', 'BrTrimtape=OFF', fileName]
    #print(printCmd)
    output = subprocess.run(printCmd, capture_output=False)
    return output.returncode


#### Main

if(len(sys.argv) != 3):
    print("Please provide label and filename as argument " + str(sys.argv))
    sys.exit(1)

labelNumber = sys.argv[1]
nameTagFileName = "/test_labels/" + sys.argv[2]

print("Printing test label")

labelName = readLabelFile(labelNumber)
print("LabelType: " + labelNumber)

if(printFile(nameTagFileName, labelName) == 0):
    blinkGreen()

