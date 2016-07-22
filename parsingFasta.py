from misc import sanitize

import re
from time import time
import subprocess as sb

integer = re.compile("[0-9]+")

#___________________________________________

#Default phylogeny is GreenGenes'
def getNextRank(rank,ranks):
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
def getBackBacteria(string,i):
    ls = string.split("__")
    n = len(ls)
    if not len(ls) == 2:
        return None,None,i
    rank = ls[0].upper()
    #Phylogeny does not include the node itself
    if rank == "S":
        return None,ls[1],i
    if not ls[1]:
        name = "Unnamed_" + "%s"%i
        return (name,rank),None,str(int(i)+1)
    return (ls[1],rank),None,i

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
#Greengenes' phylogeny: ranks in order of increasing accuracy
def parseFasta(filename,ranks=["S","G","F","O","C","P","K","R"]):
    start = time()
    i = 0
    otuList = [ int(i) for i in sb.check_output("awk '/; otu_[0-9]*/' meta/" + filename + ".fasta | awk -F '; ' '{ print $NF }' | sed 's/otu_//g'",shell=True).split() if integer.match(i) ][:: -1]
    idList = [ int(i) for i in sb.check_output("awk '/>/' meta/" + filename + ".fasta | cut -d ' ' -f 1 | sed 's/>//g'",shell=True).split() if integer.match(i) ][::-1]
    sb.call("awk '/>/' meta/" + filename + ".fasta | sed 's/\"//g' | sed \"s/\'//g\" | sed 's/otu_[0-9]*//g' | sed 's/^>[0-9]* [A-Z][A-Z]*[0-9]*[.][0-9]* //g' | sed 's/[;]//g' > meta/newfile.fasta",shell=True)
    idSequences = dict.fromkeys([])
    nodesDict = dict.fromkeys([("Root","R")])
    otuDict = dict.fromkeys([])
    paths = []
    with open("meta/newfile.fasta","r") as fo:
        for line in fo:
            if not idList:
                print "\n/!\ ERROR: Parsing error in fasta file (1)."
                raise ValueError
            identifier = idList.pop()
            ls = line.split("k__")
            if not (len(ls) == 2):
                print "\n/!\ ERROR: Parsing Fasta error (2)."
                raise ValueError
            ls[1] = "k__" + ls[1]
            #deletes white spaces
            name = cleanName(ls[0])
            if not name:
                break
            currPhylogeny = []
            for x in ls[1].split(" "):
                bact,nameBact,i = getBackBacteria(x,i)
                if bact:
                    currPhylogeny.append(bact)
                    nodesDict.setdefault(bact)
            rank = getNextRank(currPhylogeny[-1][1],ranks)
            if not rank:
                break
            name = nameBact or name
            if not name:
                break
            if (rank == ranks[0]):
                paths.append([('Root','R')] + currPhylogeny + [(name,rank)])
            idSequences[identifier] = (name,rank)
            nodesDict.setdefault((name,rank))
            if not otuList:
                print "\n/!\ ERROR: Parsing error in fasta file (3)."
                raise ValueError
            otuDict.setdefault((name,rank),otuList.pop())
    sb.call("rm -f meta/newfile.fasta",shell=True)
    end = time()
    print "TIME .fasta:",(end-start),"sec"
    return idSequences,list(paths),nodesDict.keys(),otuDict
