from misc import sanitize

from time import time
import subprocess as sb
import re

integer = re.compile("[0-9]+")
phylogeny = re.compile("([r]|[k]|[p]|[c]|[o]|[f]|[g]|[s])__([a-z]|[A-Z]|[" "]|[0-9])+")

#From a string "rank__name" returns a pair (name,rank)
def getBackBacteria(string):
    ls = string.split("__")
    n = len(ls)
    if not len(ls) == 2:
        return ""
    rank = sanitize(ls[0]).upper()
    #Phylogeny does not include the node itself
    if rank == "S":
        return ""
    return (sanitize(ls[1]),rank)

#gets back names
def recomposeNameList(nameList):
    lsClean = []
    for name in nameList:
        if not phylogeny.match(name):
            if not lsClean:
                print "\n/!\ ERROR: FASTA file formatting of phylogeny is incorrect."
                raise ValueError
            lastName = lsClean.pop()
            newName = lastName + " " + name
            lsClean.append(newName)
        else:
            lsClean.append(name)
    return lsClean

#Returns the list of pairs (identifiers of sequence,name of sequence) @idSequences in the file
#and the array @phyloSequences such as @phyloSequences[i] is the phylogeny of @idSequences[i]
def parseFasta(filename):
    start = time()
    idSequences = []
    phyloSequences = []
    sb.call("sed 'n;d' meta/" + filename + ".fasta > meta/newfile.fasta",shell=True)
    fo = open("meta/newfile.fasta","r")
    r = fo.readlines()
    for line in r:
        #the FASTA file is such as:
        #first line: >identifier integer.integer name rank__name;rank__name; ...; otu_integer [phylogeny]
        #second line: sequence associated to this identifier
        currPhylogeny = []
        #deletes > part
        lsDirty = line[1:].split(" ")
        identifier = sanitize(lsDirty[0])
        #from name...
        lsDirty = lsDirty[2:]
        name = ""
        i = 0
        n = len(lsDirty)
        while lsDirty and not phylogeny.match(lsDirty[i]):
            name += sanitize(lsDirty[i]) + " "
            i += 1
        #deletes last white space
        name = name[:-1]
        #deletes "otu" part
        lsDirty = recomposeNameList(lsDirty[i:-1])
        #gets back phylogeny
        for phylo in lsDirty:
            bact = getBackBacteria(sanitize(phylo).split(";")[0])
            #if bact != ""
            if bact:
                currPhylogeny.append(bact)
        idSequences.append((identifier,name))
        phyloSequences.append(currPhylogeny)
    fo.close()
    sb.call("rm -f meta/newfile.fasta",shell=True)
    end = time()
    print "TIME .fasta:",(end-start)
    return idSequences[-1],phyloSequences[-1]

#Approximately as fast as parseFasta
def parseFastaCharByChar(filename):
    start = time()
    idSequences = []
    phyloSequences = []
    sb.call("sed 'n;d' meta/" + filename + ".fasta > meta/newfile.fasta",shell=True)
    fo = open("meta/newfile.fasta","r")
    r = fo.readlines()
    for line in r:
        #the FASTA file is such as:
        #LINE: >identifier integer.integer name rank__name;rank__name; ...; otu_integer [phylogeny]
        #deletes > part
        index = 1
        currPhylogeny = []
        indexEnd = 1
        while not line[indexEnd] == " ":
            indexEnd += 1
        #Gets identifier
        identifier = sanitize(line[index:indexEnd])
        index = indexEnd+1
        #jumping over "integer.integer" section
        while line[index] and not line[index] == " ":
            index += 1
        index += 1
        indexEnd = index + 0
        while not line[indexEnd] == "_":
            indexEnd += 1
        indexEnd -= 3
        #Gets name
        name = sanitize(line[index:indexEnd+1])
        index = indexEnd + 2
        indexEnd = index + 0
        while not line[index:index + 3] == "otu":
            indexEnd = index + 0
            while not line[indexEnd] == ";":
                indexEnd += 1
            bact = getBackBacteria(sanitize(line[index:indexEnd].split("(class)")[0]))
            if bact:
                currPhylogeny.append(bact)
            index = indexEnd + 2
        idSequences.append((identifier,name))
        phyloSequences.append(currPhylogeny)
    fo.close()
    sb.call("rm -f meta/newfile.fasta",shell=True)
    end = time()
    print "TIME .fasta:",(end-start)
    return idSequences,phyloSequences
