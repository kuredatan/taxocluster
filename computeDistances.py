from misc import getCorrespondingID,memArray,mergeList
from taxoTree import TaxoTree

#@dataArray = [samplesInfoList,infoList,idSequences,filenames,matchingNodes,paths,nodesListTree,taxoTree]

#distance(@sample1,@sample2) = |number of nodes matched in @sample1| + |number of nodes matched in @sample2| - 2*|number of nodes matched in both samples|
#@q is useless here
def dist1(sample1,sample2,dataArray,q):
    print sample1,sample2
    #@dataArray[4] = matchingNodes, dictionary of (key=sample,value=list of nodes matched in this sample)
    nodes1 = dataArray[4].get(sample1)
    print "/!\ Got access to matching nodes (1)..."
    nodes2 = dataArray[4].get(sample2)
    print "/!\ Got access to matching nodes (2)..."
    common = [x for x in nodesList1 if memArray(x,nodesList2)]
    print "/!\ Got common nodes..."
    return len(nodesList1) + len(nodesList2) - 2*len(common)

#distance(@sample1,@sample2) = |L1| + |L2| - q*(|N1interM2| + |N2interM1|) - |M1interM2| (see README for notations)
def dist2(sample1,sample2,dataArray,q):
    print sample1,sample2
    #@dataArray[4] = matchingNodes, dictionary of (key=sample,value=list of nodes matched in this sample)
    nodes1 = dataArray[4].get(sample1)
    nodes2 = dataArray[4].get(sample2)
    nodeLCA1 = taxoLCA(paths,nodesList1)
    nodeLCA2 = taxoLCA(paths,nodesList2)
    #@dataArray[7] = taxoTree
    #Looking for the subtree rooted at the LCA of the matched nodes
    tree1 = dataArray[7].search(nodeLCA1[0],nodeLCA1[1])
    tree2 = dataArray[7].search(nodeLCA2[0],nodeLCA2[1])
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
        m1 = memArray(x,nodes1)
        m2 = memArray(x,nodes2)
        if m1 and m2:
            commonMatchedNodes += 1
        elif m1:
            specificNodes2 += 1
        elif m2:
            specificNodes1 += 1
    return leavesNumber1 + leavesNumber2 - q*(specificNodes1 + specificNodes2) - commonMatchedNodes
