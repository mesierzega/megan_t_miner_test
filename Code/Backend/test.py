import ds4se.facade as facade
import os
import sys
import ast
#changing file to test it

def new_probability(num1, num2):   #written as a function to be more easily updated to a different algorithm later
    return (num1+num2)/2

def outputValues(model, values):
     with open(os.getcwd() + sys.argv[3], 'w', encoding='latin1') as writeFile:
        for key in values:
            if (float(values[key]) >= outputThreshold):
                print("Source File: ",key, "Target File: ", targetFilename, "Traceability: ",values[key])
                writeFile.write("Model:"+ model + "\tSource File: " + key + ", Target File: " + targetFilename + ", Traceability: " + str(values[key]) + '\n')
        writeFile.close()

os.chdir('../../')
sourcePath = os.getcwd() + sys.argv[1]
targetPath = os.getcwd()
targetList = open(os.getcwd() + sys.argv[2], 'r', encoding='latin1').read().splitlines()
outputThreshold = float(sys.argv[4]) 
input = ast.literal_eval(sys.argv[5]) #the dictionary with (targetFile, sourceFile) -- a tuple -- as the key and the probability as the value
#dictionary to be filled later

for targetFilename in targetList:
    with open(os.path.join(targetPath, targetFilename), 'r', encoding='latin1') as f: # open in readonly mode
        targetData = f.read()
        f.close()
    valuesWMD = {}   #can change variable names to be more general later so models can be replaced
    valuesSCM = {}
    valuesDoc = {}
    for sourceFilename in os.listdir(sourcePath):
        with open(os.path.join(sourcePath,sourceFilename), 'r', encoding='latin1') as f:
            sourceData = f.read()
            f.close()

        resultWMD = facade.TraceLinkValue(sourceData,targetData,"word2vec", "WMD")
        resultSCM = facade.TraceLinkValue(sourceData,targetData,"word2vec", "SCM")
        resultDoc = facade.TraceLinkValue(sourceData,targetData,"doc2vec")
        traceResultWMD = resultWMD[1]
        traceResultSCM = resultSCM[1]
        traceResultDoc = resultDoc[1]
        tmpStr = targetFilename+" "+sourceFilename
        if tmpStr in input:  #check if the file pair is in the input from the user
            traceResultWMD = new_probability(traceResultWMD, float(input[tmpStr]))  #recalculating the probability
            traceResultSCM = new_probability(traceResultSCM, float(input[tmpStr]))
            traceResultDoc = new_probability(traceResultDoc, float(input[tmpStr]))
        # print("Source File: ",sourceFilename, "Target File: ", targetFilename, "Traceability: ",result)

    # new code added to keep track of/print just the four links with the highest traceability values
        valuesWMD[sourceFilename] = traceResultWMD
        valuesSCM[sourceFilename] = traceResultSCM
        valuesDoc[sourceFilename] = traceResultDoc

    outputValues("word2vec, metric = WMD", valuesWMD)
    outputValues("word2vec, metric = SCM", valuesSCM)
    outputValues("doc2vec", valuesDoc)
   
