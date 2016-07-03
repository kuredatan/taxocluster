#Implements K-means algorithm
import numpy as np
from misc import inf,getCorrespondingID

#@dist is the distance used to compute calculus
#@elementSet is the set of elements to cluster
#@k is the number of clusters required (it will likely be the number of clusters obtained by partitionning the set of elements by the values of metadata)
#@startingSet is a list of k elements that will represent the means of each cluster (these elements will be likely be k elements which values of metadata are known)
#Returns the k clusters and the distance matrix
def updateMean(meanSample,cluster,distanceMatrix,totalElementSet):
    meanDistance = 0
    n = len(cluster)
    for sample1 in cluster

def kMeans(elementSet,k,kClusters,startSet,dist,dataArray,q=0.5):
    totalElementSet = elementSet + startSet
    meanSamples = [(x,getCorrespondingID(x,totalElementSet)) for x in kClusters]
    n = len(totalElementSet)
    #Computes the distance matrix
    distanceMatrix = np.zeros((n,n))
    for i1 in range(n):
        #dist is symmetric
        for i2 in range(i1+1,n):
            s = dist(totalElementSet[i1],totalElementSet[i2],dataArray)
            distanceMatrix[i1][i2] = s
            distanceMatrix[i2][i1] = s
    for sample in elementSet:
        id1 = getCorrespondingID(sample,totalElementSet)
        minDist = inf
        minCluster = None
        for i in range(k):
            distance = distanceMatrix[meanSamples[i][1]][id1]
            if distance < minDist:
                minDist = distance
                minCluster = i
        kClusters[minCluster].append(sample)
        meanSamples[minCluster] = updateMean(meanSamples[minCluster],kCluster[minCluster])
    return kClusters,distanceMatrix
    
                
                
        
