from time import time
import sys as s
import re

from misc import sanitize

integer = re.compile("[0-9]+")

def parseMatch2(filename):
    allSequences = dict.fromkeys((None,None))
    fo = open("meta/match/" + filename + ".match","r")
    r = fo.readlines()
    #Each line corresponds to a read of this patient
    for read in r:
        index = 0
        while not read[index] == " ":
            index += 1
        index += 1
        ls = [ int(i) for i in read[index:100].split(" ") if integer.match(i)]
        while not read[index] == "\n":
            indexEnd = index + 0
            while not read[indexEnd] == " " and not read[indexEnd] == "\n":
                indexEnd += 1
            if read[indexEnd] == "\n":
                break    
            s = sanitize(read[index:indexEnd])
            if integer.match(s) and not (int(s) in allSequences):
                allSequences.setdefault(int(s))
            index = indexEnd + 1
    fo.close()
    sequences = [k for k in allSequences.keys() if k]
    return (filename,sequences)

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
    #return allMatches

def test():
    from parsingInfo import parseInfo
    samplesInfoList,_ = parseInfo("Info")
    samplesIDList = [sample[0] for sample in samplesInfoList]
    parseAllMatch([samplesIDList[0]])
