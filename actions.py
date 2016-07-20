from __future__ import division
import numpy as np
import re

from writeOnFiles import writeFile
from taxoTree import TaxoTree,printTree
from misc import isInDatabase,partitionSampleByMetadatumValue,cleanClusters,trimList,convertClustersIntoGraph,sanitize
from computeDistances import dist1,dist2
from dotModule import graphNO
from compareClusters import compareCluster,compareCenters
from kMeans import kMeans
 
#@dataArray = [samplesInfoList,infoList,idSequences,filenames,matchingNodes,paths,nodesListTree,taxoTree,dist1Dict,dist2Dict]

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
#@dataArray = [samplesInfoList,infoList,idSequences,filenames,matchingNodes,paths,nodesListTree,taxoTree]

#Actions
#Improvement will include a whole list of metadata to cluster
def clusteringAct(dataArray):
    print dataArray[1]
    metadatum = sanitize(raw_input("Select the metadatum among those above to cluster the set of samples. [e.g. " + dataArray[1][0] + "]\n")).split(";")[0]
    isInDatabase([metadatum],dataArray[1])
    valueSet,clusters = partitionSampleByMetadatumValue([metadatum],dataArray[1],dataArray[0])
    #that is, k in K-means Algorithm
    numberClass = len(valueSet)
    startSet = [cluster[0] for cluster in clusters]
    #Selects the starting samples of each cluster
    kClusters = [[cluster[0]] for cluster in clusters]
    trimmedList = trimList(dataArray[3],startSet)
    print "/!\ Clustering with the first distance..."
    #@distanceInClusters is a list of lists of (sample,sum of all distances from this sample to others samples in the same cluster)
    #@dataArray[8] = dist1Dict
    kClusters,_,distanceDict,distanceInClusters = kMeans(trimmedList,numberClass,kClusters,startSet,dataArray[8],dataArray)
    print "-- End of first clustering --"
    #Deletes samples in cluster that are too far from the others
    kClusters = cleanClusters(kClusters,distanceInClusters)
    sampleSet = []
    for cluster in kClusters:
        sampleSet += cluster
    startSet = [cluster[0] for cluster in kClusters]
    kClusters = [[start] for start in startSet]
    trimmedList = trimList(sampleSet,startSet)
    q = int(sanitize(raw_input("Choose parameter q between 0 and 1.\n")))
    if q < 0 or q > 1:
        print "\n/!\ ERROR: You should choose q between 0 and 1."
        raise ValueError
    print "/!\ Clustering with the second distance..."
    #@distanceMatrix is the distance dictionary (key=(sample1,sample2),value=distance between sample1 and sample2)
    #@dataArray[9] = dist2Dict
    kClusters,meanSamples,distanceDict,_ = kMeans(trimmedList,numberClass,kClusters,startSet,dataArray[9],dataArray,q)
    print "-- End of second clustering --"
    print "Printing the",numberClass,"clusters:"
    i = 1
    #@kClusters contains the list of the k clusters. Each cluster is a list of sample IDs
    for cluster in kClusters:
        print "\n-- Cluster #",i
        print "Size:",len(cluster)
        for x in cluster:
            print x
        i += 1
    print "Score of the clustering (comprised between 0 and 1):"
    print "The more it is close to 1, the more the clustering is relevant."
    #The clustering obtained with the K-Means method
    kClusterCopy = [cluster for cluster in kClusters]
    #The clustering obtained by comparing the values of the metadatum
    clustersCopy = [cluster for cluster in clusters]
    #Score by using first method of comparison
    compareClusterScore = 0
    if not (len(kClustersCopy) == k == len(clustersCopy)):
        print "\n/!\ ERROR: Length error in clustering:",k,len(kClustersCopy),len(clustersCopy),"."
        raise ValueError
    while kClusterCopy and clustersCopy:
        cl1 = kClusterCopy.pop()
        cl2 = clustersCopy.pop()
        compareClusterScore += compareCluster(cl1,cl2)
    compareClusterScore = compareClusterScore/k
    #Score by using second method of comparison
    compareCentersScore = compareCenters(meanSamples,distanceDict,numberClass)
    print "Compare clusters score is:",compareClusterScore,"."
    print "Compare centers score is:",compareCentersScore,"."
    answer = raw_input("Do you want to save the results? Y/N\n")
    if (answer == "Y"):
        answer2 = raw_input("Do you want to compute the sets of common nodes for each cluster? [It can be considered relevant when the score of comparing clusters is at least over 0.5] Y/N\n")
        commonList = extractCommonNodes(kClusters,dataArray)
        data = "**** CLUSTERS FOR METADATUM " + metadatum + "WITH VALUES: " + str(valueSet)
        i = 1
        for cluster in kClusters:
            data += "\n\n-- Cluster #" + str(i)
            data += "\nSize: " + str(len(cluster))
            if (answer2 == "Y"):
                data += "\nSet of common nodes: " + str(commonList[i]) 
            for x in cluster:
                data += "\n" + str(x)
            i += 1
        data += "\n\nCompare clusters score is:" + str(compareClustersScore)
        data += "\n\nCompare centers score is:" + str(compareCentersScore)
        data += "END OF FILE ****"
        writeFile(data)
        graph = convertClustersIntoGraph(kClusters,distanceDict,trimmedList,startSet)
        graphNO(graph)
    elif not (answer == "N"):
        print "/!\ You should answer by Y or N."
#____________________________________________________________________________

def printTreeAct(dataArray):
    printTree(dataArray[7])
