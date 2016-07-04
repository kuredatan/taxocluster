from misc import getCorrespondingID,mem
#Tools to compare clusters produced by K-Means Algorithm

#The more the coefficient returned is close to 1, the more the clusters are alike
#Returns |common samples between the two clusters|/|samples of the two clusters|
def compareCluster(cluster1,cluster2):
    commonSamples = [sample for sample in cluster1 if mem(sample,cluster2)]
    return len(commonSamples)/(len(cluster1) + len(cluster2) - len(commonSamples))

#compares the distance between two centers @meanSample1 and @meanSample2 relatively to the distances between each pair of clusters
def compareCenters(meanSample1,meanSample2,totalElementSet,distanceMatrix):
    id1 = getCorrespondingID(meanSample1)
    id2 = getCorrespondingID(meanSample2)
    #+normalization
    
