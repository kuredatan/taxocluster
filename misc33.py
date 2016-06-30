from __future__ import division
import numpy as np
import re

from writeOnFiles import writeFile

inf = 100000000000000

integer = re.compile("[0-9]+")

def truncate(number, digitNumber):
    #Splitting the decimal and the integer parts of @number
    numberStringed = str(number).split('.')
    decimal = numberStringed[-1]
    integer = numberStringed[0]
    #Care not to write the "." in the case where no decimal is required
    if digitNumber >= len(decimal):
        return int(integer)
    else:
        return float(integer + "." + decimal[:digitNumber])

#Gets sample IDs from the data matrix
#/!\ Some of the samples may be appear in the data matrix!
def getSampleIDList(samplesList):
    sampleIDList = []
    for sample in samplesList:
        if not mem(sample[0],sampleIDList):
            sampleIDList.append(sample[0])
    #Sorts sample IDs in alphabetical order
    return sorted(sampleIDList,key=lambda x:x)

def sanitize(name):
    ls = name.split(" ")
    if (len(ls) == 1):
        return ls[0]
    sName = ""
    sLs = []
    for l in ls:
        if not (l == "" or l == "(class)" or l == "\n" or l == "#" or l == ";"):
            sLs.append(l)
    for l in sLs[:-1]:
        sName = sName + l + " "
    sName = sName + sLs[-1]
    return sName.split("\n")[0]

#is member function
def mem(x,ls):
    n = len(ls)
    for i in range(n):
        if (x == ls[i]):
            return True
    return False

#Checks if the elements in @parselist belong to @datalist else returns an error
def isInDatabase(parseList,dataList):
    for pl in parseList:
        if not mem(pl,dataList):
            n = len(dataList)
            if not n:
                print "\n/!\ ERROR: [BUG] [actions/isInDatabase] Empty list."
            else:
                print "\n/!\ ERROR: '" + str(pl) + "' is not in the database beginning with: " + str(dataList[:min(n-1,3)]) + "."
            raise ValueError


#Given a set of samples, gives the list of disjoint groups of samples according to the value of the metadatum, and the set of values of the metadatum
#@metadatum is a list (of one element) of metadata.
def partitionSampleByMetadatumValue(metadatum,infoList,samplesInfoList):
    #One metadatum only!
    metadatum = metadatum[0]
    #computes the number of column which matches the metadatum in infoList
    i = 0
    n = len(infoList)
    while i < n and not (infoList[i] == metadatum):
        i += 1
    if (i == n):
        print "\n/!\ ERROR: metadatum",metadatum,"not found"
        raise ValueError
    #Getting the set of values of the metadatum
    #Sorting samples according to the values of the metadatum
    sampleSorted = sorted(samplesInfoList,key=lambda x: x[i])
    #List of list of samples: one sublist matches a value of the metadatum
    valueSampleMetadatum = []
    #The set of values of the metadatum
    valueSet = []
    if not len(sampleSorted):
        print "\n/!\ ERROR: You have selected no sample."
        raise ValueError
    sample = sampleSorted.pop()
    if len(sample) < i:
        print "\n/!\ ERROR: [BUG] [misc/partitionSampleByMetadatumValue] Different lengths",len(sample),"and",i,"(1)"
        raise ValueError
    #selects a sample where the value of the metadatum is known
    while not integer.match(sample[i]):
        sample = sampleSorted.pop()
        if len(sample) < i:
            print "\n/!\ ERROR: [BUG] [misc/partitionSampleByMetadatumValue] Different lengths",len(sample),"and",i,"(2)"
            raise ValueError
    #Initializing the set of values of the metadatum
    currValue = sample[i]
    valueSet.append((metadatum,int(currValue)))
    #While it remains samples in the list
    while sampleSorted:
        valueSample = []
        isEmpty = False
        #Filling the list of samples with similar values of the metadatum
        while sampleSorted and (sample[i] == currValue):
            valueSample.append(sample)
            sample = sampleSorted.pop()
            #gets the next sample where the value of the metadatum is known
            while not integer.match(sample[i]) and sampleSorted:
                sample = sampleSorted.pop()
            #If sampleSorted is empty
            if not sampleSorted:
                isEmpty = True
        #appends the newly created list to the main list
        valueSampleMetadatum.append(valueSample)
        #Initializing next loop with the new different value of the metadatum
        currValue = sample[i]
        if isEmpty:
            #Adding this value to the set
            valueSet.append((metadatum,int(currValue)))
    return valueSet,valueSampleMetadatum
