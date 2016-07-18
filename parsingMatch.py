from time import time
import sys as s
import re
import subprocess as sb
import numpy as np
import array

integer = re.compile("[0-9]+")

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename,i):
    print filename
    start = time()
    number = int(sb.check_output("head -n 1 ./meta/match/testfiles/file" + str(i) + ".test",shell=True))
    result = np.zeros(number)
    index = 0
    with open("./meta/match/testfiles/file" + str(i) + ".test","r+b") as fo:
        isFirst = True
        for read in fo:
            if isFirst:
                isFirst = False
            else:
                iterator = re.finditer(integer,read)
                for i in iterator:
                    result[index] = int(i.group(0))
                    index += 1
    end = time()
    print "TIME:",(end-start)
    return (filename,result)

#Returns dictionary @allMatches (key=sample ID a.k.a. @filename,value=list of identifiers of sequences matching a read in this sample) 
def parseAllMatch(filenames):
    allMatches = dict.fromkeys((None,None))
    start = time()
    filenames = sorted(filenames,key=lambda x:x)
    i = 0
    for filename in filenames:
        try:
            if filename:
                sampleID,sequencesArray = parseMatch(filename,i)
                allMatches.setdefault(sampleID,sequencesArray)
                i += 1
        except IOError:
            print "\nERROR: Maybe the filename",filename,".match does not exist in \"meta/matches\" folder\n"
            s.exit(0)
    end = time()
    print "TIME .match:",(end-start)
    return allMatches
