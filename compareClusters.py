from misc import getCorrespondingID
#Tools to compare clusters produced by K-Means Algorithm

#The more the coefficient returned is close to 1, the more the clusters are alike
#Returns |common nodes between the two clusters|/|nodes of the two clusters|
def compareCluster1(cluster1,cluster2):
    commonNodes = []
