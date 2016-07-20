from misc import sanitize

import re
from time import time
import subprocess as sb

integer = re.compile("[0-9]+")

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
        return None,None
    rank = ls[0].upper()
    #Phylogeny does not include the node itself
    if rank == "S":
        return None,ls[1]
    return (ls[1],rank),None

#__________________________________________

import subprocess as sb
import re

stringLit = re.compile("[a-z][a-z]*")

def cleanName(dName):
    while dName and not stringLit.match(dName[0].lower()):
        dName = dName[1:]
    while dName and not stringLit.match(dName[-1]):
        dName = dName[:-1]
    if not dName:
        return None    
    return dName

#_________________________________________

#LINE: >identifier integer.integer name rank__name;rank__name; ...; otu_integer [phylogeny]

#Returns @idSequences dictionary (key=identifier of sequence,value=((name of associated sequence/node,rank of node),phylogeny of node)
def parseFasta(filename):
    start = time()
    sb.call("sed 'n;d' meta/" + filename + ".fasta | sed 's/\"//g' | sed \"s/\'//g\" | sed \'s/ str[.]//g\' | sed \'s/ sp[.]//g\' | sed 's/>//g' | sed 's/otu_[0-9]*//g'| sed 's/[A-Z][A-Z][A-Z]*[0-9]*//g' | sed 's/[A-Z][A-Z][A-Z]*[0-9]* [0-9]*//g' | sed 's/(.)//g' | sed 's/[-][0-9][0-9]*[A-Z]*//g' | sed 's/[A-Z][A-Z][A-Z]*[0-9]*[.][0-9]*//g' | sed 's/[0-9]*[.][0-9]*//g'  | sed 's/[;]//g' | sed 's/[A-Z] //g' > meta/newfile.fasta",shell=True)
    idList = [ int(i) for i in sb.check_output("cut -d ' ' -f 1 meta/newfile.fasta",shell=True).split() if integer.match(i) ][::-1]
    idSequences = dict.fromkeys([])
    with open("meta/newfile.fasta","r") as fo:
        for line in fo:
            identifier = idList.pop()
            ls = line.split("k__")
            if not (len(ls) == 2):
                print "\n/!\ ERROR: Parsing Fasta error."
                raise ValueError
            ls[1] = "k__" + ls[1]
            #deletes white spaces
            name = cleanName(ls[0])
            if not name:
                break
            currPhylogeny = []
            for x in ls[1].split(" "):
                bact,nameBact = getBackBacteria(x)
                if bact:
                    currPhylogeny.append(bact)
            rank = getNextRank(currPhylogeny[-1][1])
            if not rank:
                break
            idSequences.setdefault(identifier,(nameBact or name,rank))
    sb.call("rm -f meta/newfile.fasta",shell=True)
    end = time()
    print "TIME .fasta:",(end-start)
    return idSequences
