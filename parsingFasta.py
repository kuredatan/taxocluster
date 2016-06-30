from misc import sanitize
from time import time

import re

integer = re.compile("[0-9]+")
phylogeny = re.compile("([r]|[k]|[p]|[c]|[o]|[f]|[g]|[s])__([a-z]|[A-Z]|[" "]|[0-9])+")

#From a string "rank__name" returns a pair (name,rank)
def getBackBacteria(string):
    ls = string.split("__")
    n = len(ls)
    if not len(ls) == 2:
        print "\n/!\ ERROR: FASTA file formatting error."
        raise ValueError
    return (sanitize(ls[1]),sanitize(ls[0]).upper())

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
    file_fasta = open("meta/" + filename + ".fasta","r")
    lines = file_fasta.readlines()
    file_fasta.close()
    fileLength = len(lines)
    k = 0
    while k < fileLength:
        #the FASTA file is such as:
        #first line: >identifier integer.integer name rank__name;rank__name; ...; otu_integer [phylogeny]
        #second line: sequence associated to this identifier
        currPhylogeny = []
        #deletes > part
        lsDirty = lines[k][1:].split(" ")
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
            currPhylogeny.append(getBackBacteria(sanitize(phylo).split(";")[0]))
        idSequences.append((identifier,name))
        phyloSequences.append(currPhylogeny)
        k += 2
    end = time()
    print "TIME .fasta:",(end-start)
    return idSequences,phyloSequences
