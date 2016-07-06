from time import time
import sys as s
import mmap as m

from misc import sanitize

def parseMatch2(filename):
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
    fo.close()
    return (filename,allSequences)

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename):
    allSequences = []
    fo = open("meta/match/" + filename + ".match","r")
    r = fo.readlines()
    #Each line corresponds to a read of this patient
    for read in fo:
        lsDirty = read.split(" ")
        lsClean = []
        #Last string is "\n"
        for string in lsDirty[:-1]:
            lsClean.append(sanitize(string))
        if len(lsClean) < 1:
            print "\n/!\ ERROR: MATCH parsing error:",len(lsClean),"."
            raise ValueError
        allSequences += lsClean[1:]
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
            #s.exit(0)
    end = time()
    print "TIME .match:",(end-start)
    #return allMatches

def test():
    from parsingInfo import parseInfo
    samplesInfoList,_ = parseInfo("Info")
    samplesIDList = [sample[0] for sample in samplesInfoList]
    parseAllMatch(samplesIDList)
