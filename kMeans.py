from __future__ import division
#Implements K-means algorithm
import numpy as np
from misc import inf,getCorrespondingID,mem
from random import randint
from copy import deepcopy

#@dist is the distance used to compute calculus
#@elementSet is the set of elements to cluster
#@k is the number of clusters required (it will likely be the number of clusters obtained by partitionning the set of elements by the values of metadata)
#@startingSet is a list of k elements that will represent the means of each cluster (these elements will be likely be k elements which values of metadata are known)
#Returns the k clusters and the distance matrix

#Clusters are ordered
def shouldStop(kClusters,previouskClusters,k):
    endIt = True
    i = 0
    while i < k:
        endIt = endIt and (set(kClusters[i]) == set(previouskClusters[i]))
        i += 1
    return endIt

def updateMean(meanSample,cluster,distanceMatrix,totalElementSet,n):
    meanDistance = 0
    nodes = 0
    m = len(cluster)
    if not m:
        print "\n/!\ ERROR: Empty cluster."
        raise ValueError
    for i in range(m):
        id1 = getCorrespondingID(cluster[i],totalElementSet,n)
        for j in range(i+1,m):
            id2 = getCorrespondingID(cluster[j],totalElementSet,n)
            nodes += 1
            meanDistance += distanceMatrix[id1][id2]
    meanDistance = meanDistance/nodes
    currMean = cluster[0]
    idMean = getCorrespondingID(currMean,totalElementSet,n)
    maxNodesAtMeanDistance = len([sample for sample in cluster[1:] if distanceMatrix[getCorrespondingID(sample,totalElementSet,n)][idMean] <= meanDistance])
    for sample1 in cluster[1:]:
        id1 = getCorrespondingID(sample1,totalElementSet,n)
        numberNodesAtMeanDistance = len([sample for sample in cluster if not (sample == sample1) and distanceMatrix[getCorrespondingID(sample,totalElementSet,n)][id1] <= meanDistance])
        if numberNodesAtMeanDistance > maxNodesAtMeanDistance:
            currMean = sample1
            idMean = id1
            maxNodesAtMeanDistance = numberNodesAtMeanDistance
    return (currMean,idMean)

def dist(a,b,c):
    return (ord(a)+ord(b))/2+ord(a)-ord(b)

#@startSet solves the problem of initialization in K-Means Algorithm
def kMeans(elementSet,k,kClusters,startSet,dist,dataArray,q=0.5):
    totalElementSet = elementSet + startSet
    n = len(totalElementSet)
    meanSamples = [(x[0],getCorrespondingID(x[0],totalElementSet,n)) for x in kClusters]
    #Computes the distance matrix
    distanceMatrix = np.zeros((n,n))
    for i1 in range(n):
        #dist is symmetric
        for i2 in range(i1+1,n):
            s = dist(totalElementSet[i1],totalElementSet[i2],dataArray)
            distanceMatrix[i1][i2] = s
            distanceMatrix[i2][i1] = s
    endIt = False
    previouskClusters = deepcopy(kClusters)
    iteration = 0
    while not endIt:
        for i in range(n-k):
            id1 = getCorrespondingID(elementSet[i],totalElementSet,n)
            minDist = inf
            minCluster = None
            for p in range(k):
                meanID = meanSamples[p][1]
                distance = distanceMatrix[meanID][id1]
                if distance < minDist:
                    minDist = distance
                    minCluster = p
            #Deleting element from another cluster
            for clusterID in range(k):
                if mem(elementSet[i],kClusters[clusterID]):
                    kClusters[clusterID] = [sample for sample in kClusters[clusterID] if not (sample == elementSet[i])]
            kClusters[minCluster].append(elementSet[i])
            meanSamples[minCluster] = updateMean(meanSamples[minCluster],kClusters[minCluster],distanceMatrix,totalElementSet,n)
        endIt = shouldStop(kClusters,previouskClusters,k)
        previouskClusters = deepcopy(kClusters)
        iteration += 1
    return kClusters,meanSamples,totalElementSet,distanceMatrix
