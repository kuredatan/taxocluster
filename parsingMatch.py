from time import time
import sys as s
import re

from misc import sanitize

integer = re.compile("[0-9]+")

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename):
    allSequences = []
    fo = open("meta/match/" + filename + ".match","r")
    r = fo.readlines()
    numberRead = 0
    #Each line corresponds to a read of this patient
    for read in r:
        print numberRead
        lsDirty = read.split(" ")
        lsClean = []
        #Last string is "\n"
        for string in lsDirty[1:-1]:
            s = sanitize(string)
            if integer.match(s):
                lsClean.append(int(s))
        if len(lsClean) > 0:
            allSequences += lsClean
        numberRead += 1
    print allSequences[:100]
    fo.close()
    return (filename,allSequences)

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
    #return allMatches
