from misc import sanitize

import re
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
    return (ls[1],rank)

#__________________________________________

#LINE: >identifier integer.integer name rank__name;rank__name; ...; otu_integer [phylogeny]

#Returns @idSequences dictionary (key=identifier of sequence,value=((name of associated sequence/node,rank of node),phylogeny of node)
def parseFasta(filename):
    start = time()
    sb.call("sed 'n;d' meta/" + filename + ".fasta | sed 's/>//g' | sed 's/[A-Z][A-Z][0-9]*[.][0-9]*//g' | sed 's/otu_[0-9]*//g' > meta/newfile.fasta",shell=True)
    idSequences = dict.fromkeys((None,(None,None)))
    with open("meta/newfile.fasta","r") as fo:
        for line in fo:
            index = 1
            while not (line[index] == " "):
                index += 1
            identifier = int(line[:index])
            ls = line[index+1:].split("k__")
            if not (len(ls) == 2):
                print "/n/!\ ERROR: Parsing Fasta error."
                raise ValueError
            ls[1] = "k__" + ls[1]
            name = ls[0]
            currPhylogeny = [ bact for bact in map(getBackBacteria,ls[1].split("; ")) if bact]
            rank = getNextRank(currPhylogeny[-1][1])
            idSequences.setdefault(identifier,((name,rank),currPhylogeny))
    sb.call("rm -f meta/newfile.fasta",shell=True)
    end = time()
    print "TIME .fasta:",(end-start)
    return idSequences
