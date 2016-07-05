from misc import getCorrespondingID,mem,mergeList
from taxoTree import TaxoTree
#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes,paths,n,nodesListTree,taxoTree]

#MISSING LINK BETWEEN SAMPLES IN @MATCHINGNODES AND @FEATURESVECTORLIST
def convertFeaturesIntoMatching(featuresVectorList,matchingNodes,sampleID):
    return sampleID

def convertMatchingIntoFeatures(featuresVectorList,matchingNodes,sampleID):
    return sampleID

#distance(@sample1,@sample2) = |number of nodes matched in @sample1| + |number of nodes matched in @sample2| - 2*|number of nodes matched in both samples|
#@q is useless here
def distance1(sample1,sample2,dataArray,q):
    sample11 = convertFeaturesIntoMatching(dataArray[4],dataArray[5],sample1)
    sample22 = convertFeaturesIntoMatching(dataArray[4],dataArray[5],sample2)
    samplesList = [x[0] for x in dataArray[5]]
    n = len(samplesList)
    id1 = getCorrespondingID(sample11,samplesList,n)
    id2 = getCorrespondingID(sample22,samplesList,n)
    nodesList1 = dataArray[5][id1]
    nodesList2 = dataArray[5][id2]
    common = [x for x in nodesList1 if mem(x,nodesList2)]
    return len(nodesList1) + len(nodesList2) - 2*len(common)

#distance(@sample1,@sample2) = |L1| + |L2| - q*(|N1interM2| + |N2interM1|) - |M1interM2| (see README for notations)
def distance2(sample1,sample2,dataArray,q):
    sample11 = convertFeaturesIntoMatching(dataArray[4],dataArray[5],sample1)
    sample22 = convertFeaturesIntoMatching(dataArray[4],dataArray[5],sample2)
    samplesList = [x[0] for x in dataArray[5]]
    n = len(samplesList)
    id1 = getCorrespondingID(sample11,samplesList,n)
    id2 = getCorrespondingID(sample22,samplesList,n)
    nodesList1 = dataArray[5][id1]
    nodesList2 = dataArray[5][id2]
    nodeLCA1 = taxoLCA(paths,nodesList1)
    nodeLCA2 = taxoLCA(paths,nodesList2)
    #@dataArray[9] = taxoTree
    #Looking for the subtree rooted at the LCA of the matched nodes
    tree1 = dataArray[9].search(nodeLCA1[0],nodeLCA1[1])
    tree2 = dataArray[9].search(nodeLCA2[0],nodeLCA2[1])
    leaves1,leavesNumber1 = tree1.leaves(False)
    leaves2,leavesNumber2 = tree2.leaves(False)
    #M1interM2
    commonMatchedNodes = 0
    #N1interM2
    specificNodes1 = 0
    #N2interM1
    specificNodes2 = 0
    leaves = mergeList(leaves1,leaves2)
    for x in leaves:
        m1 = mem(x,nodesList1)
        m2 = mem(x,nodesList2)
        if m1 and m2:
            commonMatchedNodes += 1
        elif m1:
            specificNodes2 += 1
        elif m2:
            specificNodes1 += 1
    return leavesNumber1 + leavesNumber2 - q*(specificNodes1 + specificNodes2) - commonMatchedNodes
