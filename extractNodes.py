from misc import getCorrespondingID,mem

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes,paths,n,nodesListTree,taxoTree]
def isCommon(node,k,nodesListList):
    b = True
    i = 1
    while b and i < k:
        b = mem(node,nodesListList[i])
        i += 1
    return b

def extractNodesInCluster(cluster,samplesList,n,k,dataArray):
    common = []
    nodesListList = []
    for sample in cluster:
        id1 = getCorrespondingID(sample,samplesList,n)
        nodesListList.append(dataArray[5][id1])
    if not nodesListList:
        print "\n/!\ ERROR: Cluster is empty."
        raise ValueError
    for x in nodesListList[0]:
        if isCommon(x,k,nodesListList[1:]):
            common.append(x)
    return common

#Returns the sets of common nodes in each cluster @commonList
#@commonList[i] is the set of common nodes for cluster @clusters[i]
#Improvement would exactly indicate which nodes are discrimant for the clustering
def extractCommonNodes(clusters,dataArray):
    samplesList = [x[0] for x in dataArray[5]]
    commonList = []
    n = len(samplesList)
    k = len(clusters)
    for cluster in clusters:
        commonList.append(extractNodesInCluster(cluster,samplesList,n,k,dataArray))
    return commonList
