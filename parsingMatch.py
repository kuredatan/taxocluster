from time import time
import sys as s
import re
import subprocess as sb
import numpy as np

def generateDTYPE(line):
    numberColumns = sb.call("tr ' ' '\n' " + line + " | wc -l",shell=True)
    dtype = []
    for i in range(numberColumns):
        dtype.append(("n%d"%i,np.uint32))
    return dtype

integer = re.compile("[0-9]+")

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename):
    print filename
    start = time()
    sb.call("cut -d ' ' -f 2- ./meta/match/" + filename + ".match | sed 's/\n/ /g' > ./meta/match/file.test",shell=True)
    print "done"
    numberRows = int(sb.check_output("wc -l ./meta/match/" + filename + ".match",shell=True).split()[0])
    numberColumns = sb.call("head -1 ./meta/match/file.test | tr ' ' '\n' | wc -l",shell=True)
    result = np.zeros(numberColumns*numberRows)
    print "done"
    print numberColumns,np.shape(result)
    index = 0
    with open("./meta/match/file.test","r+b") as fo:
        for line in fo:
            ls = line.split()
            for i in ls:
                result[index] = int(i)
                index += 1
            break
    end = time()
    sb.call("rm -f *.mmap_match")
    print "TIME:",(end-start)
    return (filename,result)

#Returns dictionary @allMatches (key=sample ID a.k.a. @filename,value=list of identifiers of sequences matching a read in this sample) 
def parseAllMatch(filenames):
    allMatches = dict.fromkeys((None,None))
    start = time()
    for filename in filenames:
        try:
            if filename:
                sampleID,sequencesList = parseMatch(filename)
                allMatches.setdefault(sampleID,sequencesList)
        except IOError:
            print "\nERROR: Maybe the filename",filename,".match does not exist in \"meta/matches\" folder\n"
            s.exit(0)
    end = time()
    print "TIME .match:",(end-start)
    return allMatches
