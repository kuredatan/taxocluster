import sys as s

from parsingMatch import parseAllMatch
from parsingFasta import parseFasta
from misc import mem

#Creates for each patient the corresponding features vector and matching nodes, that is:
#@featuresVectorList is the list of @featuresVector such as @featuresVector is a pair
#(@name of sample/patient,list of (metadatum,value for this patient in the data matrix) pairs)
#and @matchingNodes is the list of pairs (name of patient,list of nodes matched in this sample that is a (name,rank) list)

#Default phylogeny is GreenGenes'
def getNextRank(rank,ranks=["R","K","P","C","O","F","G","S"]):
    i = 0
    n = len(ranks)
    while i < n and not (rank == ranks[i]):
        i += 1
    if (i == n):
        print "\n/!\ ERROR: Wrong phylogeny (1). Please change the ranks array in featuresVector.py."
        raise ValueError
    elif (i == n-1):
        #print "\n/!\ ERROR: Wrong phylogeny (2). Please change the ranks array in featuresVector.py."
        #raise ValueError
        return ranks[i]
    else:
        return ranks[i+1]

#@idSequences is a list of (identifier,name of node associated to sequence) pairs
def getCorrespondingID(sequenceID,idSequences):
    i = 0
    n = len(idSequences)
    while i < n and not idSequences[i][0] == sequenceID:
        i += 1
    if (i == n):
        #ignore these ID (for tests only)
        print "\n/!\ ERROR: sequenceID ",sequenceID," not in idSequences."
        #raise ValueError
        return -1
    return i

def getNodeAssociated(sequenceID,idSequences,phyloSequences):
    index = getCorrespondingID(sequenceID,idSequences)
    if index == -1:
        #ignore these IDs
        return 0
    if not (len(phyloSequences[index][-1]) == 2):
        print "\n/!\ ERROR: [BUG] [featuresVector/getNodeAssociated] Wrong node length:",len(phyloSequences[index][-1]),"."
        raise ValueError
    fatherRank = phyloSequences[index][-1][1]
    rank = getNextRank(fatherRank)
    if not (len(idSequences[index]) == 2):
        print "\n/!\ ERROR: [BUG] [featuresVector/getNodeAssociated] Wrong pair length:",len(idSequences[index]),"."
        raise ValueError
    name = idSequences[index][1]
    return (name,rank)

#Returns @nodesList, the list of matched nodes (name,rank)
#@idSequences is a list of (identifier,name of sequence)
#@phyloSequences is a list of lists of (name,rank) such as @phyloSequences[i] is the phylogeny of @idSequences[i]
def getNodesList(idSequences,phyloSequences):
    nodesList = []
    for identName in idSequences:
        if not len(identName) == 2:
            print "\n/!\ ERROR: Incorrect idSequences formatting."
            raise ValueError
        node = getNodeAssociated(identName[0],idSequences,phyloSequences)
        if not node:
            #Ignore these samples
            continue
        else:
            nodesList.append(node)
    return nodesList

#@allMatches is a list of (sample ID,list of sequences ID matching a read in this sample) pairs (see parsingMatch.py)
#returns a list of (sample ID,list of nodes (name,rank) matching a read in this sample) pairs
#@nodesList is such as @nodesList[i] is the node associated to sequence idSequences[i] (see @getNodesList)
def getMatchingNodes(allMatches,nodesList,idSequences):
    matchingNodes = []
    for pair in allMatches:
        if not len(pair) == 2:
            print "\n/!\ ERROR: Incorrect matches formatting."
            raise ValueError
        sampleID = pair[0]
        matchingSequences = pair[1]
        matchingThisSampleNodes = []
        for sequenceID in matchingSequences:
            index = getCorrespondingID(sequenceID,idSequences)
            matchingThisSampleNodes.append(nodesList[index])
        matchingNodes.append((sampleID,matchingThisSampleNodes))
    return matchingNodes
        
#Returns @featuresVectorList and @matchingNodes
#@filenames is the list of .match file names
#@fastaFileName is a string of the .fasta file name
def featuresCreate(sampleInfoList,infoList,filenames,fastaFileName):
    print "/!\ Parsing .match files"
    print "[ You may have to wait a few minutes... ]"
    allMatches = parseAllMatch(filenames)
    print "/!\ Parsing .fasta files"
    print "[ You may have to wait a few minutes... ]"
    try:
        idSequences,phyloSequences = parseFasta(fastaFileName)
    except IOError:
        print "\nERROR: Maybe the filename",fastaFileName,".fasta does not exist in \"meta\" folder\n"
        s.exit(0)
    #Link between file name and sample name?
    #--------------CONSTRUCTING @featuresVectorList
    featuresVectorList = []
    for sample in sampleInfoList:
        n = len(sample)
        if n < 1:
            print "\n/!\ ERROR: Sample info incorrect."
            raise ValueError
        metadataList = []
        for i in range(1,n):
            metadataList.append((infoList[i],sample[i]))
        featuresVectorList.append((sample[0],metadataList))
    #--------------CONSTRUCTING @matchingNodes
    nodesList = getNodesList(idSequences,phyloSequences)
    matchingNodes = getMatchingNodes(allMatches,nodesList,idSequences)
    return featuresVectorList,matchingNodes,nodesList

def test():
    from parsingInfo import parseInfo
    sampleInfoList,infoList = parseInfo("Info")
    featuresVectorList,matchingNodes,nodesList = featuresCreate(sampleInfoList,infoList,["test"],"test")
    return featuresVectorList[:3],matchingSequences[:3]
