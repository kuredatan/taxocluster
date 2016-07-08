from time import time
import sys as s
import re

from misc import sanitize
import mmap

integer = re.compile("[0-9]+")

def parseMatch5(filename):
    allSequences = dict.fromkeys((None,None))
    with open("meta/match/" + filename + ".match","r+b") as fo:
        #m = mmap.mmap(fo.fileno(),0,prot=mmap.PROT_READ)
        #read = map.readline()
        #Each line corresponds to a read of this patient
        for read in fo:
            lsDirty = read.split(" ")
            #Last string is "\n"
            for string in lsDirty[:-1]:
                s = sanitize(string)
                if integer.match(s) and not (int(s) in allSequences):
                    allSequences.setdefault(int(s))
            #read = map.readline()
    seq = [k for k in allSequences if k]
    return (filename,seq)

def parseMatch6(filename):
    allSequences = []
    with open("meta/match/" + filename + ".match","r+b") as fo:
        #lines = fo.readlines()
        #Each line corresponds to a read of this patient
        for read in file_match:
            index = 0
            while not (read[index] == " "):
                index += 1
            index += 1
            try:
                indexEnd = index + 0
                while not (read[indexEnd] == " "):
                    indexEnd += 1
                s = sanitize(read[index:indexEnd])
                if integer.match(s) and not (int(s) in allSequences):
                    allSequences.append(int(s))
            except IndexError:
                continue
    return (filename,allSequences)

def parseMatch4(filename):
    allSequences = []
    with open("meta/match/" + filename + ".match","r+b") as fo:
        #lines = fo.readlines()
        #Each line corresponds to a read of this patient
        for read in fo:
            lsDirty = read.split(" ")
            for string in lsDirty[:-1]:
                s = sanitize(string)
                if integer.match(s) and not (int(s) in allSequences):
                    allSequences.append(int(s))
    return (filename,allSequences)

def parseMatch3(filename):
    allSequences = dict.fromkeys((None,None))
    with open("meta/match/" + filename + ".match","r+b") as fo:
        #m = mmap.mmap(fo.fileno(),0,prot=mmap.PROT_READ)
        #r = fo.readlines()
        for read in iter(map.readline(),""):
            index = 0
            while not read[index] == " ":
                index += 1
            index += 1
            ls = [ int(r) for r in read[index:].split(" ") if integer.match(r) and not (int(r) in allSequences) ]
            for i in ls:
                allSequences.setdefault(i)
    sequences = [k for k in allSequences.keys() if k]
    return (filename,sequences)

def parseMatch2(filename):
    allSequences = dict.fromkeys((None,None))
    with open("meta/match/" + filename + ".match","r+b") as fo:
        #m = mmap.mmap(fo.fileno(),0,prot=mmap.PROT_READ)
        r = fo.readlines()
        for read in r:
            index = 0
            while not read[index] == " ":
                index += 1
            index += 1
            try:
                while not read[index] == " ":
                    indexEnd = index + 0
                    while not read[indexEnd] == " ":
                        indexEnd += 1
                    s = sanitize(read[index:indexEnd])
                    if integer.match(read[index:indexEnd]) and not (int(s) in allSequences):
                        allSequences.setdefault(int(s))
                    index = indexEnd + 1
            except IndexError:
                continue
    sequences = [k for k in allSequences.keys() if k]
    return (filename,sequences)

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename):
    allSequences = dict.fromkeys((None,None))
    with open("meta/match/" + filename + ".match","r+b") as fo:
        r = fo.readlines()
        #Each line corresponds to a read of this patient
        for read in r:
            lsDirty = read.split(" ")
            #Last string is "\n"
            for string in lsDirty[1:-1]:
                s = sanitize(string)
                if integer.match(s) and not (int(s) in allSequences):
                    allSequences.setdefault(int(s))
    sequences = [k for k in allSequences.keys() if k]
    return (filename,sequences)

#Returns the list @allMatches such as @allMatches[i] is a pair (identifier of patient,list of identifiers of sequences matching a read in this patient) 
def parseAllMatch(filenames,number=1):
    n = len(filenames)
    number = 1
    allMatches = []
    start = time()
    for filename in filenames:
        try:
            print number,"/",n
            if filename:
                if number == 1:
                    allMatches.append(parseMatch(filename))
                elif number == 2:
                    allMatches.append(parseMatch2(filename))
                elif number == 3:
                    allMatches.append(parseMatch3(filename))
                elif number == 4:
                    allMatches.append(parseMatch4(filename))
                elif number == 5:
                    allMatches.append(parseMatch5(filename))
                elif number == 6:
                    allMatches.append(parseMatch6(filename))
            number += 1
        except IOError:
            print "\nERROR: Maybe the filename",filename,".match does not exist in \"meta/matches\" folder\n"
            s.exit(0)
    end = time()
    print "TIME .match:",(end-start)
    return allMatches

def test(number=1):
    from parsingInfo import parseInfo
    samplesInfo,_ = parseInfo("Info")
    samplesID = [sample[0] for sample in samplesInfo]
    _ = parseAllMatch(samplesID[0:1],number)
