import numpy as np

from misc import getCorrespondingID,memList,mergeList,taxoLCA,inf
from taxoTree import TaxoTree
from writeOnFiles import writeFile

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
    _,number,numberl1,numberl2 = memList(nodes1,nodes2)
    print "/!\ Got common nodes..."
    return numberl1 + numberl2 - 2*number

#distance(@sample1,@sample2) = |L1| + |L2| - q*(|N1interM2| + |N2interM1|) - |M1interM2| (see README for notations)
def dist2(sample1,sample2,dataArray,q):
    print sample1,sample2
    #@dataArray[4] = matchingNodes, dictionary of (key=sample,value=list of nodes matched in this sample)
    nodes1 = dataArray[4].get(sample1)
    nodes2 = dataArray[4].get(sample2)
    print len(nodes1),len(nodes2)
    print "start taxoLCA"
    nodeLCA1 = taxoLCA(dataArray[7].paths,nodes1)
    print "end taxoLCA (1)"
    nodeLCA2 = taxoLCA(dataArray[7].paths,nodes2)
    print "end taxoLCA(2)"
    #@dataArray[7] = taxoTree
    #Looking for the subtree rooted at the LCA of the matched nodes
    #that is the "induced tree"
    if not nodeLCA1 or not nodeLCA2:
        return inf
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
    matchedBy1,_,_,_ = memList(leaves,nodes1)
    matchedBy2,_,_,_ = memList(leaves,nodes2)
    _,numberCommon,number1,number2 = memList(matchedBy1,matchedBy2)
    return leavesNumber1 + leavesNumber2 - q*(number1 + number2) - numberCommon

#__________________________________________________________________________

#@dataArray = [samplesInfoList,infoList,idSequences,filenames,matchingNodes,paths,nodesListTree,taxoTree]

def computeDistanceMatrix(dist,dataArray):
    q = 0.5
    if dist == dist2:
        q = float(raw_input("Choose the value of q to compute [q should be between 0 and 1].\n"))
        if q > 1 or q < 0:
            print "\n/!\ ERROR: Wrong value of q [ shoudl be between 0 and 1 ]:",q,"."
            raise ValueError
    n = len(dataArray[3])
    matrix = np.zeros((n,n))
    #distance is symmetric
    for i in range(n):
        for j in range(i+1,n):
            #dataArray[3] = filenames
            distance = dist(dataArray[3][i],dataArray[3][j],dataArray,q)
            matrix[i][j] = distance
            matrix[j][i] = distance
    writeFile(matrix,"Distance matrix","matrix")
