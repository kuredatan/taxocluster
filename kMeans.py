from __future__ import division
#Implements K-means algorithm
import numpy as np
from random import randint
from copy import deepcopy
from time import time

from misc import inf

#@dist is the distance used to compute calculus
#@elementSet is the set of elements to cluster
#@k is the number of clusters required (it will likely be the number of clusters obtained by partitionning the set of elements by the values of metadata)
#@kClusters is a list of k elements that will represent the means of each cluster (these elements will be likely be k elements which values of metadata are known)
#Returns the k clusters, the distance dictionary (key=(sample1,sample2),value=distance between sample1 and sample2)

#Clusters are ordered
def shouldStop(kClusters,previouskClusters,k):
    endIt = True
    i = 0
    while i < k:
        endIt = endIt and (set(kClusters[i]) == set(previouskClusters[i]))
        i += 1
    return endIt

#The mean sample of a cluster is the one that minimizes the distance to the other samples
def updateMean(cluster,distanceDict):
    distanceInCluster = []
    minDistance = inf
    currMean = None
    if not cluster:
        print "\n/!\ ERROR: Empty cluster."
        raise ValueError
    for samplei in cluster:
        distanceToThisSample = 0
        for samplej in set(cluster):
            if not (samplej == samplei):
                d = distanceDict.get((samplei,samplej))
                if d:
                    distanceToThisSample += d
                #else:
                    #print samplei,samplej
        distanceInCluster.append((samplei,distanceToThisSample))
        if distanceToThisSample < minDistance:
            minDistance = distanceToThisSample + 0
            currMean = samplei
    return currMean,distanceInCluster

def getClusters(currAssignments,k,totalElementSet):
    kClusters = [None] * k
    n = len(totalElementSet)
    for i in range(n):
        if not kClusters[currAssignments[i]]:
            kClusters[currAssignments[i]] = [totalElementSet[i]]
        else:
            kClusters[currAssignments[i]].append(totalElementSet[i])
    return kClusters

#@startSet solves the problem of initialization in K-Means Algorithm
def kMeans(elementSet,k,kClusters,startSet,distanceDict,dataArray,meanSamples=None):
    start = time()
    totalElementSet = elementSet + startSet
    n = len(totalElementSet)
    if (n > len(dataArray[3])):
        print "\n/!\ ERROR: Different lengths of set of samples",n,len(dataArray[3]),"."
        raise ValueError
    #Initialization of the clusters and the means
    meanSamples = meanSamples or [x for x in startSet]
    endIt = False
    previouskClusters = deepcopy(kClusters)
    #currAssignments[i] is the index of the cluster where totalElementSet[i] currently is
    currAssignments = [None]*(n-k) + [i for i in range(k)]
    #distanceInClusters is a list of lists of (sample,sum of all distances from this samples to any other sample in the same cluster) pairs
    distanceInClusters = [None]*k
    print "/!\ Starting clustering..."
    while not endIt:
        print "/!\ Next iteration",currAssignments,"."
        for unassignedElement in range(n-k):
            minDist = inf
            minCluster = None
            for clusterIndex in range(k):
                distance = distanceDict.get((meanSamples[clusterIndex],totalElementSet[unassignedElement]))
                #In case of "infinite" distance for every cluster, the element would be assigned nowhere if the condition was distance < minDist
                if distance <= minDist:
                    minDist = distance
                    minCluster = clusterIndex
            #Deletes the element from another cluster, if it exists
            currAssign = currAssignments[unassignedElement]
            #Meaning the element has already been assigned to another cluster
            if currAssign and not (currAssign == minCluster):
                newCluster = []
                for x in kClusters[currAssign]:
                    if not (x == totalElementSet[unassignedElement]) and not (x in newCluster):
                        newCluster.append(x)
                kClusters[currAssign] = newCluster
                meanSamples[currAssign],distanceInCluster = updateMean(kClusters[currAssign],distanceDict)
                distanceInClusters[currAssign] = distanceInCluster
            #If the element is unassigned (minCluster =/= None and currAssign == None => currAssign =/= minCluster)
            elif not (currAssign == minCluster):
                currAssignments[unassignedElement] = minCluster
                newCluster = []
                for x in kClusters[minCluster]:
                    if not (x in newCluster) and not (x == totalElementSet[unassignedElement]):
                        newCluster.append(x)
                    elif (x == totalElementSet[unassignedElement]):
                        print "/!\ ERROR:",x,"is in cluster #",currAssign," whereas it should not be assigned to any cluster."
                kClusters[minCluster] = newCluster + [totalElementSet[unassignedElement]]
                meanSamples[minCluster],distanceInCluster = updateMean(kClusters[minCluster],distanceDict)
                distanceInClusters[minCluster] = distanceInCluster
            #else currAssign == minCluster, nothing should be done
        endIt = shouldStop(kClusters,previouskClusters,k)
        previouskClusters = deepcopy(kClusters)
    print "-- End of clustering."
    end = time()
    print "TIME:",(end-start)
    kClusters = getClusters(currAssignments,k,totalElementSet)
    return kClusters,meanSamples,distanceDict,distanceInClusters
