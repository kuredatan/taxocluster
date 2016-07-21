import sys as s

from parsingMatch import parseAllFact
from parsingFasta import parseFasta

def sanitizeNode(node):
    if not node or not (len(node) == 2):
        #It means this node cannot appear in the taxonomic tree
        return None
    else:
        return node 
        
#@allMatches is a dictionary of (key=sample ID,value=list of sequences ID matching a read in this sample)
#@idSequences is a dictionary of (key=identifier of node,value=(name,rank of node))
#@filenames is the list of .match file names == list of samples ID /!\
#Returns a dictionary of (key=sample ID,value=list of nodes (name,rank) matching a read in this sample)
def getMatchingNodes(allMatches,idSequences,filenames):
    matchingNodes = dict.fromkeys(filenames)
    for sample in filenames:
        matchingSequencesID = allMatches.get(sample)
        matchingNodesInThisSample = []
        if not (matchingSequencesID == None):
            for sequenceID in matchingSequencesID:
                node = idSequences.get(sequenceID)
                cleanNode = sanitizeNode(node)
                if cleanNode:
                    matchingNodesInThisSample.append(cleanNode)
            matchingNodes[sample] = matchingNodesInThisSample
        else:
            print "The sample \'",sample,"\' could not be processed."
    return matchingNodes
        
#Returns @matchingNodes, dictionary of (key=sample ID,value=list of nodes matched in this sample -i.e. at least in one read of this sample), and @idSequences, which is a dictionary of (key=identifier of sequence,value=(name,rank) of the node associated to this sequence)
#@filenames is the list of .match file names == list of samples ID /!\
#@fastaFileName is a string of the .fasta file name
#@sampleIDList is the list of samples ID
def featuresCreate(filenames,fastaFileName):
    print "/!\ Parsing .match files"
    print "[ You may have to wait a few seconds... ]"
    #@allMatches is a dictionary of (key=sample ID,value=list of sequences ID matching a read in this sample)
    import time
    start = time.time()
    allMatches = parseAllFact(filenames)
    end = time.time()
    print "TIME:",(end-start),"sec"
    print "/!\ Parsing .fasta files"
    print "[ You may have to wait a few seconds... ]"
    try:
        #@idSequences is a dictionary of (key=identifier,value=((name,rank))
        #@paths is the list of paths from root to leaves
        #@nodesListTree is the list of all nodes (internal nodes and leaves) in the tree
        #We do not care for now of the OTU
        idSequences,paths,nodesListTree,_ = parseFasta(fastaFileName)
    except IOError:
        print "\nERROR: Maybe the filename",fastaFileName,".fasta does not exist in \"meta\" folder\n"
        s.exit(0)
    matchingNodes = getMatchingNodes(allMatches,idSequences,filenames)
    print "/!\ Matching nodes list done."
    return matchingNodes,idSequences,paths,nodesListTree
