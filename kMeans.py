#Implements K-means algorithm

#@dist is the distance used to compute calculus
#@elementSet is the set of elements to cluster
#@k is the number of clusters required (it will likely be the number of clusters obtained by partitionning the set of elements by the values of metadata)
#@startingSet is a list of k elements that will represent the means of each cluster (these elements will be likely be k elements which values of metadata are known)
def kMeans(elementSet,k,startingSet,dist,dataArray):
    for sample in elementSet:
        
