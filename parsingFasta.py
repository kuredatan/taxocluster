from misc import sanitize

from time import time
import subprocess as sb

#___________________________________________

#Default phylogeny is GreenGenes'
def getNextRank(rank,ranks=["S","G","F","O","C","P","K","R"]):
    i = 0
    n = len(ranks)
    while i < n and not (rank == ranks[i]):
        i += 1
    if (i == n):
        #print "\n/!\ ERROR: Wrong phylogeny (1). Please change the ranks array in featuresVector.py:",rank,"."
        #raise ValueError
        return None
    elif (i == n-1):
        print "\n/!\ ERROR: Wrong phylogeny (2). Please change the ranks array in featuresVector.py."
        raise ValueError
    else:
        return ranks[i-1]
#___________________________________________

#From a string "rank__name" returns a pair (name,rank)
def getBackBacteria(string):
    ls = string.split("__")
    n = len(ls)
    if not len(ls) == 2:
        return None
    rank = ls[0].upper()
    #Phylogeny does not include the node itself
    if rank == "S":
        return None
    return (sanitize(ls[1]),rank)

#__________________________________________

#Returns @idSequences dictionary (key=identifier of sequence,value=((name of associated sequence/node,rank of node),phylogeny of node)
def parseFasta(filename):
    start = time()
    idSequences = dict.fromkeys((None,(None,None)))
    #Deletes the sequence part
    sb.call("sed 'n;d' meta/" + filename + ".fasta > meta/newfile.fasta",shell=True)
    with open("meta/newfile.fasta","r") as fo:
        for line in fo:
            #The FASTA file is such as:
            #LINE: >identifier integer.integer name rank__name;rank__name; ...; otu_integer [phylogeny]
            #Deletes > part
            index = 1
            currPhylogeny = []
            indexEnd = 1
            while not line[indexEnd] == " ":
                indexEnd += 1
            #Gets identifier
            identifier = line[index:indexEnd]
            index = indexEnd+1
            #Jumping over "integer.integer" section
            while line[index] and not line[index] == " ":
                index += 1
            index += 1
            indexEnd = index + 0
            #While not encountering the phylogeny section
            while not line[indexEnd] == "_":
                indexEnd += 1
            indexEnd -= 3
            #Gets name
            name = sanitize(line[index:indexEnd+1])
            index = indexEnd + 2
            indexEnd = index + 0
            #Gets phylogeny
            while not line[index:index + 3] == "otu":
                indexEnd = index + 0
                while not line[indexEnd] == ";":
                    indexEnd += 1
                bact = getBackBacteria(line[index:indexEnd])
                if bact:
                    currPhylogeny.append(bact)
                index = indexEnd + 2
            rank = getNextRank(currPhylogeny[-1][1])
            idSequences.setdefault(identifier,((name,rank),currPhylogeny))
    sb.call("rm -f meta/newfile.fasta",shell=True)
    end = time()
    print "TIME .fasta:",(end-start)
    return idSequences
