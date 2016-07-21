#@dataArray = [samplesInfoList,infoList,idSequences,filenames,matchingNodes,paths,nodesListTree,taxoTree,distMatchedDict,distConsensusDict]

#@node is a (name,rank) pair
#@nodesListList is a list of lists of (name,rank) pairs
#@n = len(@nodesListList)
def isCommon(node,nodesListList,n):
    b = True
    i = 0
    while b and i < n:
        b = (node in nodesListList[i])
        i += 1
    return b

#@cluster is the considered cluster
def extractNodesInCluster(cluster,dataArray):
    #the resulting list of common nodes
    commonToCluster = []
    nodesListList = []
    for sample in cluster[:-1]:
        #@dataArray[4] = matchingNodes
        #samples in matchingNodes are in the same order as in filenames
        #matchingNodes is a dictionary of (key=sample,value=list of nodes matched in this sample)
        nodesListList.append(dataArray[4].get(sample))
    if not len(nodesListList):
        print "\n/!\ ERROR: Cluster is empty."
        raise ValueError
    nodesTestList = dataArray[4].get(cluster[-1])
    n = len(nodesListList)
    for node in nodesTestList:
        if isCommon(node,nodesListList,n):
            commonToCluster.append(node)
    return commonToCluster

#Returns the sets of common nodes in each cluster @commonList
#@commonList[i] is the set of common nodes for cluster @clusters[i]
#Improvement would exactly indicate which nodes are discrimant for the clustering
def extractCommonNodes(clusters,dataArray):
    commonList = []
    for cluster in clusters:
        commonList.append(extractNodesInCluster(cluster,dataArray))
    return commonList
