from __future__ import division
#Implements K-means algorithm
import numpy as np
from misc import inf,mem
from random import randint
from copy import deepcopy

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
def updateMean(meanSample,cluster,distanceDict):
    distanceInCluster = []
    minDistance = inf
    currMean = 0
    if not cluster:
        print "\n/!\ ERROR: Empty cluster."
        raise ValueError
    for samplei in cluster:
        distanceToThisSample = 0
        for samplej in cluster:
            if not (samplej == samplei):
                distanceToThisSample += distanceDict.get((samplei,samplej))
        distanceInCluster.append((samplei,distanceToThisSample))
        if distanceToThisSample < minDistance:
            minDistance = distanceToThisSample + 0
            currMean = samplei
    return currMean,distanceInCluster

#@startSet solves the problem of initialization in K-Means Algorithm
def kMeans(elementSet,k,kClusters,startSet,dist,dataArray,q=0.5):
    totalElementSet = elementSet + startSet
    n = len(totalElementSet)
    if not (n == len(dataArray[3])):
        print "\n/!\ ERROR: Different lengths of set of samples",len(dataArray[3]),n,"."
        raise ValueError
    meanSamples = [x for x in startSet]
    #Computes the distance dictionary (key=(sample1,sample2),distance between sample1 and sample2)
    distanceDict = dict.fromkeys((None,None))
    for i1 in range(n):
        #dist is symmetric
        for i2 in range(i1+1,n):
            s = dist(totalElementSet[i1],totalElementSet[i2],dataArray,q)
            distanceDict.setdefault((totalElementSet[i1],totalElementSet[i2]),s)
            distanceDict.setdefault((totalElementSet[i2],totalElementSet[i1]),s)
    endIt = False
    previouskClusters = deepcopy(kClusters)
    #currAssignments[i] is the index of the cluster where totalElementSet[i] currently is
    currAssignments = [None]*(n-k)
    #distanceInClusters is a list of lists of (sample,sum of all distances from this samples to any other sample in the same cluster) pairs
    distanceInClusters = []*k
    while not endIt:
        for unassignedElement in range(n-k):
            minDist = inf
            minCluster = None
            for clusterIndex in range(k):
                distance = distanceDict.get(meanSamples[clusterIndex],totalElementSet[unassignedElement])
                if distance < minDist:
                    minDist = distance
                    minCluster = clusterIndex
            #Deletes the element from another cluster, if it exists
            currAssign = currAssignments[i]
            #Meaning the element has already been assigned to another cluster
            if not (currAssign == minCluster) and currAssign:
                kClusters[currAssign] = [x for x in kClusters[currAssign] if not (x == totalElementSet[i])]
            currAssignments[i] = minCluster
            kClusters[minCluster].append(totalElementSet[i])
            meanSamples[minCluster],distanceInCluster = updateMean(meanSamples[minCluster],kClusters[minCluster],distanceDict)
            distanceInClusters[minCluster] = distanceInCluster
        endIt = shouldStop(kClusters,previouskClusters,k)
        previouskClusters = deepcopy(kClusters)
    return kClusters,meanSamples,distanceDict,distanceInClusters
