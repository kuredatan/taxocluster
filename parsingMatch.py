from time import time
import sys as s
import re

from misc import sanitize

integer = re.compile("[0-9]+")

#mmap does not change much the time of computation
def parseMatchWithMmap(filename):
    allSequences = []
    with open("meta/match/" + filename + ".match", 'rb') as fo:
        fd = m.mmap(fo.fileno(), 0, prot=mmap.PROT_READ)
        read = fd.readline()
        while read:
            lsDirty = read.split(" ")
            lsClean = []
            #Last string is "\n"
            for string in lsDirty[:-1]:
                lsClean.append(sanitize(string))
            if len(lsClean) < 1:
                print "\n/!\ ERROR: MATCH parsing error:",len(lsClean),"."
                raise ValueError
            allSequences += lsClean[1:]
            read = fd.readline()
    return (filename,allSequences)

def parseMatch2(filename):
    #Dictionnary
    allSequences = dict.fromkeys((None,None))
    fo = open("meta/match/" + filename + ".match","r")
    r = fo.readlines()
    #Each line corresponds to a read of this patient
    for read in r:
        print read[:100]
        index = 0
        #Deletes name of read
        while not read[index] == " ":
            index += 1
        index += 1
        while not read[index] == "\n":
            indexEnd = index + 1
            while not (read[indexEnd] == " " or read[indexEnd] == "\n"):
                indexEnd += 1
            l = sanitize(read[index:indexEnd])
            if integer.match(l) and not allSequences.has_key(int(l)):
                allSequences.setdefault(int(l))
            index = indexEnd + 1
        break
    fo.close()
    sequences = [k for k in allSequences.keys() if k]
    print sequences
    return (filename,sequences)

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename):
    allSequences = []
    fo = open("meta/match/" + filename + ".match","r")
    r = fo.readlines()
    #Each line corresponds to a read of this patient
    for read in r:
        lsDirty = read.split(" ")
        lsClean = []
        #Last string is "\n"
        for string in lsDirty[1:-1]:
            lsClean.append(int(sanitize(string)))
        if len(lsClean) < 1:
            print "\n/!\ ERROR: MATCH parsing error:",len(lsClean),"."
            raise ValueError
        allSequences += lsClean
        break
    print allSequences
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
                allMatches.append(parseMatch2(filename))
        except IOError:
            print "\nERROR: Maybe the filename",filename,".match does not exist in \"meta/matches\" folder\n"
            #s.exit(0)
    end = time()
    print "TIME .match:",(end-start)
    #return allMatches

def test():
    from parsingInfo import parseInfo
    samplesInfoList,_ = parseInfo("Info")
    samplesIDList = [sample[0] for sample in samplesInfoList]
    parseAllMatch([samplesIDList[0]])
