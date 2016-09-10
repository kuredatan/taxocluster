from __future__ import division
from normalization import normalizeList
#Tools to compare clusters produced by K-Means Algorithm

#The more the coefficient returned is close to 1, the more the clusters are alike
#Returns |common samples between the two clusters|/|samples of the two clusters|
def compareCluster(cluster1,cluster2,untaken):
    u = set(untaken)
    cl1 = set(cluster1) - u
    cl2 = set(cluster2) - u
    inter = len(cl1 & cl2)
    total = len(cl1 | cl2)
    if not total:
        return None
    return inter/total

#compares the distance between the two centers of the corresponding clusters relatively to the distances between each pair of clusters
#@distanceDict is a dictionary of (key=(sample1,sample2),value=distance between sample1 and sample2)
#@k is the number of clusters
#Returns a coefficient between 0 and 1. The more it is close to 0, the more the two clusterings are alike.
def compareCenters(meanSamples,distanceDict,k):
    distCenterList = []
    k = len(meanSamples)
    for i in range(k):
        for j in range(k):
            if not (i == j):
                distCenterList.append(distanceDict.get((meanSamples[i],meanSamples[j])))
    distCenterList = normalizeList(distCenterList)
    maxDistance = 0
    score = 0
    for distance in distCenterList:
        if distance > maxDistance:
            maxDistance = distance + 0
        score += distance
    score = score/(k*(k-1)*distance)
    return score
