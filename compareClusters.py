from __future__ import division
from misc import getCorrespondingID,mem
from normalization import normalizeList
#Tools to compare clusters produced by K-Means Algorithm

#The more the coefficient returned is close to 1, the more the clusters are alike
#Returns |common samples between the two clusters|/|samples of the two clusters|
def compareCluster(cluster1,cluster2):
    commonSamples = [sample for sample in cluster1 if mem(sample,cluster2)]
    return len(commonSamples)/(len(cluster1) + len(cluster2) - len(commonSamples))

#compares the distance between the two centers of the corresponding clusters relatively to the distances between each pair of clusters
def compareCenters(meanSamples,clusters,totalElementSet,distanceMatrix):
    distCenterList = []
    k = len(clusters)
    n = len(totalElementSet)
    for i in range(k):
        idMean = meanSamples[i][1]
        idCenCluster = getCorrespondingID(clusters[i],totalElementSet,n)
        distCenterList.append(distanceMatrix[idMean][idCenCluster])
    distCenterList = normalizeList(distCenterList)
    score = 0
    for distance in distCenterList:
        score += distance
    score = score/k
    return score
