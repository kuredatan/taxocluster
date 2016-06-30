from __future__ import division
import numpy as np
import re
import random as rand

from writeOnFiles import writeFile
from misc import isInDatabase,sanitize,inf
from classifier import classifyIt
from youden import countYouden,interpretIt
from randomSampling import randomChoice
from multiDimList import MultiDimList
from plottingValues import plotPie

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes]

integer = re.compile("[0-9]+")

#Parsing functions
def parseList(string):
    if not (len(string.split(",")) == 1):
        print "\n/!\ ERROR: Do not use ',' as a separator: rather use ';'."
        raise ValueError
    elif not (len(string.split(":")) == 1):
        print "\n/!\ ERROR: Do not use ':' as a separator: rather use ';'."
        raise ValueError
    return string.split(";")

def parseListNode(string):
    if not (len(string.split(":")) == 1):
        print "\n/!\ ERROR: Do not use ':' as a separator: rather use ';'."
        raise ValueError
    ls = string.split(";")
    res = []
    for node in ls:
        nodeSplit = node.split(",")
        if not (len(nodeSplit) == 2):
            print "\n/!\ ERROR: Please use ',' as a separator for name,rank of a bacteria."
            raise ValueError
        nodeSplitName = nodeSplit[0].split("(")
        if not (len(nodeSplitName) == 2):
            print "\n/!\ ERROR: Please use the syntax '([name],[rank])' for each bacteria."
            raise ValueError
        nodeSplitRank = nodeSplit[-1].split(")")
        if not (len(nodeSplitRank) == 2):
            print "\n/!\ ERROR: Please use the syntax '([name],[rank])' for each bacteria."
            raise ValueError
        name,rank = nodeSplitName[-1],nodeSplitRank[0]
        res.append((name,rank))
    return res
#___________________________________________________________________________

#Macros for formatting
#Printing pretty lists of nodes
def listNodes(nodeList):
    string = ""
    for l in nodeList[:-1]:
        string += str(l) + ", "
    string += str(nodeList[-1])
    return string

#@stringNode is assumed to be a (name,rank) pair, with name and rank being strings
#@sanitizeNode allows it to be printed "(name,rank)" and not "('name','rank')"
def sanitizeNode(stringNode):
    return "(" + stringNode[0] + "," + stringNode[1] + ")"

#____________________________________________________________________________

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes]
#See featuresVector.py and README for more details about features vectors.
#@classes and @assignedClasses are MDL (multi dimensional lists)
def userNodeSelectionAct(dataArray):
    print dataArray[1]
    metadata = parseList(raw_input("Input the metadata that will cluster the set of samples among those written above. [ e.g. " + dataArray[1][0] + ";" + dataArray[1][-1] + " ]\n"))
    isInDatabase(metadata,dataArray[1])
    nodesList = parseListNode(raw_input("Choose the group of nodes you want to consider exclusively. [ Read the taxonomic tree to help you: e.g. " + sanitizeNode(dataArray[2][-3]) + ";" + sanitizeNode(dataArray[2][1]) + ";" + sanitizeNode(dataArray[2][-1]) + " ]\n"))
    isInDatabase(nodesList,dataArray[2])
    #@shape for @assignedClasses is the same than the one for @classes
    assignedClasses,classes,shape,valueSets = classifyIt(dataArray,metadata,nodesList)
    numberClass = lenMDL(classes,shape)
    #len(dataArray[0])?
    youdenJ = countYouden(assignedClasses,classes,shape,len(dataArray[0]))
    interpretIt(youdenJ)
    answer = raw_input("Do you want to plot the classes obtained as a pie? Y/N")
    if answer == "Y":
        labels = [ "Metadata: " + str(metadata) + ", Values for each metadatum: " + str([ valueSet for valueSet in valueSets]) ]
        percentagesAs = mapMDL(assignedClasses,shape,len)
        percentages = mapMDL(classes,shape,len)
        plotPie(labels,percentagesAs,"Assignments depending on " + str(nodesList) + " to class for metadata " + str(metadata))
        plotPie(labels,percentages,"Real classes depending on " + str(nodesList) + " for metadata " + str(metadata))
    elif not (answer == "N"):
        print "\n Answer by Y or N!"
    answer = raw_input("Do you want to save the results? Y/N")
    if (answer == "Y"):
        writeFile("Youden's J statistic for this classification is: " + str(youdenJ) + "\n","Assignments depending on " + listNodes(nodesList) + " to classes for metadata " + str(metadata))
    elif not (answer == "N"):
        print "\n Answer by Y or N!"
    return assignedClasses,youdenJ

#________________________________________________________________________________________________________________________

def randomSubSamplingAct(dataArray):
    print dataArray[1]
    metadata = parseList(raw_input("Input the metadata that will cluster the set of samples among those written above. [ e.g. " + dataArray[1][0] + ";" + dataArray[1][-1] + " ]\n"))
    isInDatabase(metadata,dataArray[1])
    s = raw_input("Input the number s of random samplings.\n")
    n = raw_input("Input the number n of nodes to select at each try.\n")
    if not integer.match(s) or not integer.match(n):
        print "\n/!\ ERROR: s and n must both be integers."
        raise ValueError
    s,n = int(s),int(n)
    #Here the set of classes is a list of two lists containing the samples in C and not C
    bestClassification = []
    bestClassesList = []
    bestShape = []
    bestValuesList = []
    #Worse value for this coefficient
    currBestYouden = inf
    nodesNumber = len(dataArray[3])
    while s:
        #Randomly draw n distinct nodes among the nodes in the taxonomic tree
        nodesList = randomChoice(dataArray[2],n)
        assignedClasses,classes,shape,valueSets = classifyIt(dataArray,metadata,nodesList)
        numberClass = lenMDL(classes,shape)
        #len(dataArray[0])?
        youdenJ = countYouden(assignedClasses,classes,shape,len(dataArray[0]))
        res = numberClass - youdenJ
        if min(res,currBestYouden) == res:
            bestValuesList = []
            for i in valueSets:
                bestValuesList.append(i)
            bestClassification = []
            for i in nodesList:
                bestClassification.append(i)
            bestShape = []
            for i in shape:
                bestShape.append(i)
            currBestYouden = res
            bestClassesList = []
            for i in assignedClasses:
                bestClassesList.append(i)
        s -= 1
    interpretIt(numberClass - currBestYouden)
    if answer == "Y":
        labels = [ "Metadata: " + str(metadata) + ", Values for each metadatum: " + str([ valueSet for valueSet in valueSets]) ]
        percentagesAs = mapMDL(assignedClasses,shape,len)
        percentages = mapMDL(classes,shape,len)
        plotPie(labels,percentagesAs,"Assignments depending on " + str(nodesList) + " to class for metadata " + str(metadata))
        plotPie(labels,percentages,"Real classes depending on " + str(nodesList) + " for metadata " + str(metadata))
    answer = raw_input("Do you want to save the results? Y/N")
    if (answer == "Y"):
        writeFile("Best Youden's J statistic for this classification is: " + str(numberClass - currBestYouden) + "\nand most relevant list of nodes for this set of metadata is:" + str(bestClassification),"Assignments to classes for metadata " + str(metadata))
    elif not (answer == "N"):
        print "\n Answer by Y or N!"
    return bestClassification,(numberClass - currBestYouden),bestClassesList
