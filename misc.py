from __future__ import division
import numpy as np
import re
import numpy as np

from writeOnFiles import writeFile

inf = 100000000000000

integer = re.compile("[0-9]+")

def getCorrespondingID(element,elementList,listLength):
    i = 0
    while i < listLength and not (element == elementList):
        i += 1
    if (i == listLength):
        print "\n/!\ ERROR: ",element,"not in list."
        raise ValueError
    return i

#Return the common elements (with duplicates) to l1 and l2
#and the length of both lists and of common lists
def memList(l1,l2):
    common = []
    number,numberl1,numberl2 = 0,0,0
    l11 = sorted(l1)
    l22 = sorted(l2)
    while l11 and l22:
        x = l11.pop()
        y = l22.pop()
        if x == y:
            common.append(x)
            number += 1
            numberl1 += 1
            numberl2 += 1
        elif x > y:
            l22.append(y)
            numberl1 += 1
        else:
            l11.append(x)
            numberl2 += 1
    if l11:
        numberl1 += len(l11)
    elif l22:
        numberl2 += len(l22)
    return common,number,numberl1,numberl2
    

#converts list of clusters @kClusters into a graph (adjacency matrix)
#@distanceDict is a dictionary (key=(sample1,sample2),value=distance)
def convertClustersIntoGraph(kClusters,distanceDict,trimmedList,startingSet):
    elementList = trimmedList + startingSet
    n = len(elementList)
    #adjacency matrix
    graph = [[] * n] * n 
    for cluster in kClusters:
        m = len(cluster)
        for i1 in range(m):
            for i2 in range(i1+1,m):
                id1 = getCorrespondingID(cluster[i1],elementList,n)
                id2 = getCorrespondingID(cluster[i2],elementList,n)
                graph[i1][i2] = (cluster[i1],cluster[i2],1,distanceDict.get((samplei,samplej)))
    return graph

def cleanClusters(clusters,distanceInClusters):
    k = len(clusters)
    clustersCopy = [cluster for cluster in clusters]
    newClusters = []
    for _ in range(k):
        cluster = clustersCopy.pop()
        n = len(cluster)
        #distanceList is a list of (sample,sum of distances) pairs
        distanceList = sorted(distanceInClusters.pop(),key=lambda x: x[2])
        distanceQuartile = distanceList[:3/4*n]
        newCluster = []
        for pair in distanceQuartile:
                newCluster.append(pair[0])
        newClusters.append(newCluster)
    return newClusters
            
def truncate(number, digitNumber):
    #Splitting the decimal and the integer parts of @number
    numberStringed = str(number).split('.')
    decimal = numberStringed[-1]
    integer = numberStringed[0]
    #Care not to write the "." in the case where no decimal is required
    if digitNumber >= len(decimal):
        return int(integer)
    else:
        return float(integer + "." + decimal[:digitNumber])

#Returns a list containing elements of list1 that are not elements of list2
#If the elements in lists are tuples, it will sorted using lexigraphical order with suitable order for each projection
#Sorting allows to run in worst case complexity of O(nlog(n) + mlog(m)) where n,m are the length of the two lists
def trimList(list1,list2):
    lst1 = sorted(list1)
    lst2 = sorted(list2)
    trimList = []
    while lst1 and lst2:
        x1 = lst1.pop()
        x2 = lst2.pop()
        if (x1 < x2):
            lst1.append(x1)
        elif (x1 > x2):
            trimList.append(x1)
            lst2.append(x2)
    #At the end of the loop, at least one of the two lists is empty
    if lst1:
        #We do not care of the order at the end of the merge
        return trimList + lst1
    return trimList

#Merge the elements of both lists, deleting multiple occurrences
def mergeList(list1,list2):
    lst1 = sorted(list1)
    lst2 = sorted(list1)
    union = []
    while lst1 and lst2:
        x1 = lst1.pop()
        x2 = lst2.pop()
        if (x1 == x2):
            union.append(x1)
        elif (x1 < x2):
            union.append(x2)
            lst1.append(x1)
        else:
            union.append(x1)
            lst2.append(x2)
    #At the end of the loop, at least one of the two lists is empty
    if lst1:
        #We do not care of the order at the end of the merge
        return union + lst1
    else:
        #@ls2 may be empty
        return union + lst2

#Returns a list of (name,rank,sampleHitList) tuples associated with
#nodes of the taxonomic tree reduced to the sample sampleName
#and the number of assignments in this tree
#NB: We need to keep the whole sampleHitList (and not only the
#number associated with sampleName) in order to apply set operations (intersection, ...)
def inSample(element,sampleNameList):
    #element[1] (number associated to a sample) must be non-zero
    if not element[1]:
        print "\n/!\ ERROR: [BUG] [misc/inSample] Null element."
        raise ValueError
    #If list is empty
    if not sampleNameList:
        return False
    for name in sampleNameList:
        if (element[0] == name):
            return True
    return False

#@sampleName is a list of names of samples
#takeNodesInTree(tree,sampleName) should return the taxonomic tree reduced to the nodes assigned in sample sampleName = the list of assigned node + their sampleHitList, and the number of assignments in the reduced tree, and the number of nodes in the reduced tree
def takeNodesInTree(tree,sampleNameList):
    #@sampleHitList (see TaxoTree) is a list of (name of sample, number) pairs attached to a node of a TaxoTree
    sample = []
    numberTotalAssignments = 0
    numberNodes = 0
    queue = [ tree ]
    while queue:
        node = queue.pop()
        isInSample = []
        for x in node.sampleHitList:
            if inSample(x,sampleNameList):
                isInSample.append(x)
        #if node is in sample, ie isInSample is not empty
        if isInSample:
            sample.append((node.name,node.rank,node.sampleHitList))
            numberTotalAssignments += isInSample[0][1]
            numberNodes += 1
        queue += node.children
    return sample,numberTotalAssignments,numberNodes

#For sorting lists of nodes (name,rank) by decreasing order S > G > F > O > C > P > K > R. Returns 1 if rank1 => rank2, -1 if rank1 < rank2
#You can modify the ranks and the order by modifying the default rank array
def compare(rank1,rank2,ranks=['S','G','F','O','C','P','K','R'],ranksArrayLength=8):
    for i in range(ranksArrayLength):
        if (rank2 == ranks[i]):
            return 1
        elif (rank1 == ranks[i]):
            return -1
    print "\n/!\ ERROR: Unknown rank. Did you modify the default rank array?"
    raise ValueError

def sanitize(name):
    ls = name.split(" ")
    if (len(ls) == 1):
        return ls[0]
    sName = ""
    sLs = []
    for l in ls:
        if not (l == "" or l == "(class)" or l == "\n" or l == "#"):
            sLs.append(l)
    for l in sLs[:-1]:
        sName = sName + l + " "
    if not (sLs[-1] == "" or sLs[-1] == "(class)" or sLs[-1] == "\n" or sLs[-1] == "#"):
        sName = sName + sLs[-1]
    return sName

def containsSpecie(path,name,rank):
    for x in path:
        if (x[0] == name) and (x[1] == rank):
            return True
    return False

#@paths is the paths list of a TaxoTree
#@n = len(@paths)
def selectPath(paths,name,rank,n):
    i = 0
    while i < n and not containsSpecie(paths[i],name,rank):
	i += 1
    if (i == n):
        #print "\n/!\ ERROR: [misc/selectPath] No path for (%s,%s)."%(name,rank)
        return []
    else:
        path = []
        x = paths[i]
        #Memorizes only the part of the path that leads to (name,rank)
        n = len(x)
        i = 0
        while (i < n) and not (x[i][0] == name and x[i][1] == rank):
            path.append(x[i])
            i += 1
        return path

def isLeaf(paths,name,rank,allNodes):
    l = []
    for ls in paths:
        if containsSpecie(ls,name,rank):
            l.append(ls)
    if allNodes:
        #deletes path ending with this node
        l2 = []
        for ls in l:
            if not (ls[-1][0] == name and ls[-1][1] == rank):
                l2.append(ls)
        return (len(l2) == 0)
    else:
        #Searches which paths may lead to (name,rank)
        return (len(l) == 1)

#@initList is a list of integers
def minList(initList):
    if not initList:
        return None
    mini = initList[0]
    for x in initList[1:]:
        if mini > x:
            mini = x
    return mini

def isEqual(pathsNodes):
    b = True
    paths = [path for path in pathsNodes[1:]]
    while b and paths:
        path = paths.pop()
        b = (path[0] == pathsNodes[0][0])
    return b

def setOperations(paths,nodesList,allNodes):
    pathsNodes = []
    n = len(paths)
    for node in nodesList:
        path = selectPath(paths,node[0],node[1],n)
        if path:
            pathsNodes.append(path)
        #else:
            #print "/!\ Node",node,"not in taxonomic tree."
    print pathsNodes
    commonPath = []
    n = minList([len(path) for path in pathsNodes])
    i = 0
    #As long as paths in @pathsNodes are not empty
    while (i < n) and pathsNodes[0] and isEqual(pathsNodes):
        commonPath.append(pathsNodes[0][0])
        pathsNodes = [ path[1:] for path in pathsNodes ]
        i += 1
    print commonPath
    return commonPath,pathsNodes

#Computes LCA from the list paths of a TaxoTree
def taxoLCA(paths,nodesList,allNodes=False):
    n = len(nodesList)
    if not n:
        return []
    commonPath,_ = setOperations(paths,nodesList,allNodes)
    if not commonPath:
        return []
    return commonPath[-1]

#Checks if the elements in @parselist belong to @datalist else returns an error
def isInDatabase(parseList,dataList):
    for pl in parseList:
        if not (pl in dataList):
            n = len(dataList)
            if not n:
                print "\n/!\ ERROR: [BUG] [actions/isInDatabase] Empty list."
            else:
                print "\n/!\ ERROR: '" + str(pl) + "' is not in the database beginning with: " + str(dataList[:min(n-1,3)]) + "."
            raise ValueError
    

#Given a set of samples, gives the list of disjoint groups of samples according to the value of the metadatum, and the set of values of the metadatum
#@metadatum is a list (of one element) of metadata.
def partitionSampleByMetadatumValue(metadatum,infoList,samplesInfoList):
    #One metadatum only!
    metadatum = metadatum[0]
    #computes the number of column which matches the metadatum in infoList
    i = 0
    n = len(infoList)
    while i < n and not (infoList[i] == metadatum):
        i += 1
    if (i == n):
        print "\n/!\ ERROR: metadatum",metadatum,"not found"
        raise ValueError
    #Getting the set of values of the metadatum
    #Sorting samples according to the values of the metadatum
    sampleSorted = sorted(samplesInfoList,key=lambda x: x[i])
    #List of list of samples: one sublist matches a value of the metadatum
    valueSampleMetadatum = []
    #The set of values of the metadatum
    valueSet = []
    if not len(sampleSorted):
        print "\n/!\ ERROR: You have selected no sample."
        raise ValueError
    sample = sampleSorted.pop()
    if len(sample) < i:
        print "\n/!\ ERROR: [BUG] [misc/partitionSampleByMetadatumValue] Different lengths",len(sample),"and",i,"(1)"
        raise ValueError
    #selects a sample where the value of the metadatum is known
    while not integer.match(sample[i]):
        sample = sampleSorted.pop()
        if len(sample) < i:
            print "\n/!\ ERROR: [BUG] [misc/partitionSampleByMetadatumValue] Different lengths",len(sample),"and",i,"(2)"
            raise ValueError
    #Initializing the set of values of the metadatum
    currValue = sample[i]
    valueSet.append((metadatum,int(currValue)))
    #While it remains samples in the list
    while sampleSorted:
        valueSample = []
        isEmpty = False
        #Filling the list of samples with similar values of the metadatum
        while sampleSorted and (sample[i] == currValue):
            valueSample.append(sample)
            sample = sampleSorted.pop()
            #gets the next sample where the value of the metadatum is known
            while not integer.match(sample[i]) and sampleSorted:
                sample = sampleSorted.pop()
            #If sampleSorted is empty
            if not sampleSorted:
                isEmpty = True
        #appends the newly created list to the main list
        valueSampleMetadatum.append(valueSample)
        #Initializing next loop with the new different value of the metadatum
        currValue = sample[i]
        if isEmpty:
            #Adding this value to the set
            valueSet.append((metadatum,int(currValue)))
    return valueSet,valueSampleMetadatum
