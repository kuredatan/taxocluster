from __future__ import division
import numpy as np
import re

from writeOnFiles import writeFile
from taxoTree import TaxoTree,printTree
from misc import isInDatabase,partitionSampleByMetadatumValue,cleanClusters,trimList,convertClustersIntoGraph
from computeDistance import dist1,dist2
from dotModule import graphNO
 
#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes,paths,n,nodesListTree,taxoTree]

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

def parseIntList(string):
    if not (len(string.split(",")) == 1):
        print "\n/!\ ERROR: Do not use ',' as a separator: rather use ';'."
        raise ValueError
    elif not (len(string.split(":")) == 1):
        print "\n/!\ ERROR: Do not use ':' as a separator: rather use ';'."
        raise ValueError
    l = string.split(";")
    resultList = []
    for s in l:
        if integer.match(s):
            resultList.append(int(s))
        elif s == "+inf" or s == "-inf":
            resultList.append(s)
        else:
            print "\n/!\ ERROR: Here you can only use integers or '+inf' or '-inf'."
            raise ValueError
    return resultList

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
#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes,paths,n,nodesListTree,taxoTree]

#Actions
#Improvement will include a whole list of metadata to cluster
def clusteringAct(dataArray):
    print dataArray[1]
    metadatum = sanitize(raw_input("Select the metadatum to cluster the set of samples. [e.g. " + dataArray[1][0] + "]"))
    isInDatabase([metadatum],dataArray[1])
    #that is, k in K-means Algorithm
    valueSet,clusters = partitionSampleByMetadatumValue([metadatum],dataArray[1],dataArray[0])
    numberClass = len(valueSet)
    startSet = [cluster[0] for cluster in kClusters]
    #Selects the starting samples of each cluster
    startingSet = [[cluster[0]] for cluster in clusters]
    print "/!\ Clustering with the first distance..."
    #@distanceMatrix is the distance matrix between each pair of samples
    #@distanceInCluster is a list of lists of (sample1,sample2,distance)
    #where sample1 and sample2 belong to the same cluster
    trimmedList = trimList(dataArray[3],startSet)
    kClusters,_,distanceInCluster = kMeans(trimmedList,numberClass,startingSet,startSet,dist1,dataArray)
    print "-- End of first clustering --"
    #Deletes samples in cluster that are too far from the others
    kClusters = cleanClusters(kClusters,distanceInCluster)
    startSet = [cluster[0] for cluster in kClusters]
    startingSet = [[cluster[0]] for cluster in kClusters]
    trimmedList = trimList(dataArray[3],startSet)
    print "/!\ Clustering with the second distance..."
    kClusters,distanceMatrix,_ = kMeans(trimmedList,numberClass,startingSet,startSet,dist2,dataArray)
    print "-- End of second clustering --"
    print "Printing the",numberClass,"clusters"
    i = 1
    #@kClusters contains the list of the k clusters. Each cluster is a list of sample IDs
    for cluster in kClusters:
        print "\n-- Cluster #",i
        print "Size:",len(cluster)
        for x in cluster:
            print x
        i += 1
    answer = raw_input("Do you want to save the results? Y/N\n")
    if (answer == "Y"):
        data = "**** CLUSTERS FOR METADATUM " + metadatum + "WITH VALUES: " + str(valueSet)
        i = 1
        for cluster in kClusters:
            data += "\n\n-- Cluster #" + str(i)
            data += "\nSize: " + str(len(cluster))
            for x in cluster:
                data += "\n" + str(x)
            data += "END OF FILE ****"
        writeFile(data)
        graph = convertClustersIntoGraph(kClusters,distanceMatrix,trimmedList,startSet)
        graphNO(graph)
    elif not (answer == "N"):
        print "/!\ You should answer by Y or N."
#____________________________________________________________________________

def printTreeAct(dataArray):
    printTree(dataArray[7])
