from time import time
import sys as s
import re

from misc import sanitize

integer = re.compile("[0-9]+")

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename):
    allSequences = dict.fromkeys((None,None))
    fo = open("meta/match/" + filename + ".match","r")
    r = fo.readlines()
    #Each line corresponds to a read of this patient
    for read in r:
        lsDirty = read.split(" ")
        #Last string is "\n"
        for string in lsDirty[1:-1]:
            s = sanitize(string)
            if integer.match(s) and not (int(s) in allSequences):
                allSequences.setdefault(int(s))
    fo.close()
    sequences = [k for k in allSequences.keys() if k]
    return (filename,sequences)

#Returns the list @allMatches such as @allMatches[i] is a pair (identifier of patient,list of identifiers of sequences matching a read in this patient) 
def parseAllMatch(filenames):
    allMatches = []
    start = time()
    for filename in filenames:
        try:
            print filename
            if filename:
                allMatches.append(parseMatch(filename))
        except IOError:
            print "\nERROR: Maybe the filename",filename,".match does not exist in \"meta/matches\" folder\n"
            s.exit(0)
    end = time()
    print "TIME .match:",(end-start)
    return allMatches
