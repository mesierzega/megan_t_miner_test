import configparser
import importlib
import os
import sys

config = configparser.ConfigParser()
config.read('../../pyConfig.ini')
facade = importlib.import_module(config["Imports"]["Import1"])
traceLink = getattr(facade,config["FunctionName"]["Function"])
param1 = config["FunctionParams"]["Param1"]
param2 = config["FunctionParams"]["Param2"]
def new_probability(num1, num2):   #written as a function to be more easily updated to a different algorithm later
    return (num1+num2)/2
    
def traceabilityResult(source, target, targetFile, feedback, model, metric = None):
    with open(os.path.join(target, targetFile), 'r', encoding='latin1') as f: # open in readonly mode
        targetData = f.read()
        f.close()
    values = {}
    for sourceFilename in os.listdir(source):
        with open(os.path.join(source,sourceFilename), 'r', encoding='latin1') as f:
            sourceData = f.read()
            f.close()
        if metric is None:
            result = traceLink(sourceData,targetData, model)
        else:
            result = traceLink(sourceData,targetData, model, metric)

        traceResult = result[1]
        tmpStr = targetFile+" "+sourceFilename
        if tmpStr in input:  #check if the file pair is in the input from the user
            traceResult = new_probability(traceResult, float(feedback[tmpStr]))  #recalculating the probability

        # print("Source File: ",sourceFilename, "Target File: ", targetFilename, "Traceability: ",result)

    # new code added to keep track of/print just the four links with the highest traceability values
        values[sourceFilename] = traceResult
    return values
    
def outputValues(model, valuesDict, outputThreshold, curFile, output):
    for key in valuesDict:
        if (float(valuesDict[key]) >= outputThreshold):
            print("Source File: ",key, "Target File: ", curFile, "Traceability: ",valuesDict[key])
            output.write("Model:"+ model + "\nSource File: " + key + ", Target File: " + curFile + ", Traceability: " + str(valuesDict[key]) + '\n')
  

os.chdir('../../')
sourcePath = os.getcwd() + sys.argv[1]
targetPath = os.getcwd()
targetList = open(os.getcwd() + sys.argv[2], 'r', encoding='latin1').read().splitlines()
threshold = float(sys.argv[4]) 
feedbackSourceList = sys.argv[5].split(",")
feedbackTargetList = sys.argv[6].split(",")
feedbackNumList = sys.argv[7].split(",")
input={} #dictionary to be filled
for i in range (len(feedbackSourceList)):
    input[feedbackSourceList[i]+" "+feedbackTargetList[i]]=float(feedbackNumList[i]) #the dictionary with (targetFile sourceFile, feedbackValue)
for targetFilename in targetList:

    valuesWMD = traceabilityResult(sourcePath, targetPath, targetFilename, input, param1, param2)
    valuesSCM = traceabilityResult(sourcePath, targetPath, targetFilename, input, "word2vec", "SCM")
    valuesDoc = traceabilityResult(sourcePath, targetPath, targetFilename, input, "doc2vec")



    with open(os.getcwd() + sys.argv[3], "a+", encoding='latin1') as writeFile:

        outputValues("word2vec, metric = WMD", valuesWMD, threshold, targetFilename, writeFile)
        outputValues("word2vec, metric = SCM", valuesSCM, threshold, targetFilename, writeFile)
        outputValues("doc2vec", valuesDoc, threshold, targetFilename, writeFile)
        writeFile.close()
