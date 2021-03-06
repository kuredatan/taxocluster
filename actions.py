from __future__ import division
import numpy as np
import re

from writeOnFiles import writeFile
from taxoTree import TaxoTree,printTree
from misc import isInDatabase,partitionSampleByMetadatumValue,cleanClusters,trimList,convertClustersIntoGraph,sanitize
from dotModule import graphNO
from compareClusters import compareCluster,compareCenters
from kMeans import kMeans
from extractNodes import extractCommonNodes
 
#@dataArray = [samplesInfoList,infoList,idSequences,filenames,matchingNodes,paths,nodesListTree,taxoTree,distMatchedDict,distConsensusDict]

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
#@dataArray = [samplesInfoList,infoList,idSequences,filenames,matchingNodes,paths,nodesListTree,taxoTree,distMatchedDict,distConsensusDict]

#Actions
#Improvement will include a whole list of metadata to cluster
def clusteringAct(dataArray):
    print dataArray[1]
    metadatum = sanitize(raw_input("Select the metadatum among those above to cluster the set of samples. [e.g. " + dataArray[1][0] + "]\n")).split(";")[0]
    isInDatabase([metadatum],dataArray[1])
    valueSet,clusters1 = partitionSampleByMetadatumValue(metadatum,dataArray[1],dataArray[0])
    clusters = [[sample[0] for sample in cluster] for cluster in clusters1]
    #that is, k in K-means Algorithm
    numberClass = len(valueSet)
    print "/!\ Number of classes:",numberClass,"."
    startSet = [cluster[0] for cluster in clusters]
    #Selects the starting samples of each cluster
    kClusters = [[start] for start in startSet]
    if not (len(clusters) == numberClass):
        print "\n/!\ ERROR: Different lengths: numberClass",numberClass,"clusters:",len(clusters),"."
        raise ValueError
    trimmedList = trimList(dataArray[3],startSet)
    print "/!\ Clustering with the first distance..."
    #@distanceInClusters is a list of lists of (sample,sum of all distances from this sample to others samples in the same cluster)
    #@dataArray[8] = distMatchedDict
    kClusters,meanSamples,distanceDict,distanceInClusters = kMeans(trimmedList,numberClass,kClusters,startSet,dataArray[8],dataArray)
    print "-- End of first clustering --"
    number = 0
    for cluster in kClusters:
        for _ in cluster:
            number += 1
    if not (number == len(dataArray[3])):
        print "\n/!\ ERROR: A bug occurred during the clustering:",number,"=/=",len(dataArray[3]),"."
        raise ValueError
    #Deletes samples in cluster that are too far from the others
    kClusters,untaken = cleanClusters(kClusters,distanceInClusters)
    startSet = [cluster[0] for cluster in clusters]
    #Remove from untaken the starting samples
    untaken2 = []
    for x in untaken:
        if not (x in startSet):
            untaken2.append(x)
    untaken = untaken2
    #Remove the samples in untaken from the total set of samples
    sampleSet = []
    for cluster in kClusters:
        for x in cluster:
            if not (x in sampleSet):
                sampleSet.append(x)
    for x in startSet:
        if not (x in sampleSet):
            sampleSet.append(x)
    trimmedList = trimList(sampleSet,startSet)
    print "/!\ Clustering with the second distance..."
    #@distanceDict is the distance dictionary (key=(sample1,sample2),value=distance between sample1 and sample2)
    #@dataArray[9] = distConsensusDict
    kClusters,meanSamples,distanceDict,_ = kMeans(trimmedList,numberClass,kClusters,startSet,dataArray[9],dataArray)#,meanSamples)
    print "-- End of second clustering --" 
    number = 0
    for cluster in kClusters:
        for _ in cluster:
            number += 1
    if not (number <= len(dataArray[3])):
        print "\n/!\ ERROR: An error occurred during the clustering:",number,">",len(dataArray[3]),"."
        raise ValueError
    print "Printing the",numberClass,"clusters:"
    i = 1
    #@kClusters contains the list of the k clusters. Each cluster is a list of sample IDs
    for cluster in kClusters:
        print "\n-- Cluster #",i,"associated to",metadatum,"=",valueSet[i-1],":"
        print "Size:",len(cluster)
        print sorted(cluster)
        i += 1
    print "\nScore of the clustering (comprised between 0 and 1):"
    print "The more it is close to 1, the more the clustering is relevant."
    #The clustering obtained with the K-Means method
    kClustersCopy = [cluster for cluster in kClusters]
    #The clustering obtained by comparing the values of the metadatum
    clustersCopy = [cluster for cluster in clusters]
    #Score by using first method of comparison
    compareClusterScore = 0
    if not (len(kClustersCopy) == numberClass == len(clustersCopy)):
        print "\n/!\ ERROR: Length error in clustering:",numberClass,len(kClustersCopy),len(clustersCopy),"."
        raise ValueError
    while kClustersCopy and clustersCopy:
        cl1 = kClustersCopy.pop()
        cl2 = clustersCopy.pop()
        #clusters are non-empty
        x = compareCluster(cl1,cl2,untaken)
        if x:
            compareClusterScore += x
        else:
            compareClusterScore = None
            break
    if compareClusterScore:
        compareClusterScore = compareClusterScore/numberClass
        printClusterScore = compareClusterScore
    else:
        printClusterScore = "None"
    #Score by using second method of comparison
    #compareCentersScore = compareCenters(meanSamples,distanceDict,numberClass)
    print "Compare clusters score is:",printClusterScore,"."
    #print "Compare centers score is:",compareCentersScore,"."
    answer = raw_input("Do you want to save the results? Y/N\n")
    if (answer == "Y"):
        answer2 = raw_input("Do you want to compute the sets of common nodes for each cluster? [It can be considered relevant when the score of comparing clusters is at least over 0.5] Y/N\n")
        if (answer2 == "Y"):
            commonList = extractCommonNodes(kClusters,dataArray)
        elif not (answer2 == "N"):
            print "\n/!\ You should answer Y or N, not:",answer2,"."
        data = "**** CLUSTERS FOR METADATUM " + metadatum + " WITH VALUES: " + str(valueSet)
        i = 0
        for cluster in kClusters:
            data += "\n\n-- Cluster #" + str(i+1) + " associated to " + metadatum + " = " + str(valueSet[i]) 
            data += "\nSize: " + str(len(cluster))
            if (answer2 == "Y"):
                data += "\nSet of common nodes: " + str(commonList[i])
            data += "\n" + str(cluster)
            i += 1
        data += "\n\nCompare clusters score is: " + str(compareClusterScore)
        #data += "\n\nCompare centers score is: " + str(compareCentersScore)
        data += "\n\nEND OF FILE ****"
        print "\n/!\ Saving clusters..."
        writeFile(data)
        answer2 = raw_input("Do you want to compute the graph of the clusters? Y/N\n")
        if (answer2 == "Y"):
            print "\n/!\ Constructing the graph of the clusters..."
            #@dataArray[3] = filenames
            graph = convertClustersIntoGraph(kClusters,distanceDict,len(dataArray[3]))
            graphNO(graph)
            print "\n/!\ Done. The graph is in DOT format in \"files\" folder."
        elif not (answer2 == "N"):
            print "\n/!\ You should answer Y or N, not:",answer2,"."
    elif not (answer == "N"):
        print "/!\ You should answer by Y or N."
#____________________________________________________________________________

def printTreeAct(dataArray):
    printTree(dataArray[7])
