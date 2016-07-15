from time import time
import sys as s
import re
import mmap
import subprocess as s

integer = re.compile("[0-9]+")

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename):
    print filename
    start = time()
    s.call("cut -d ' ' -f 2- ./meta/match/" + filename + ".match > ./meta/match/file.test",shell=True)
    s.call("perl -pi -e 'chomp' ./meta/match/file.test",shell=True)
    with open("./meta/match/file.test","r+b") as fo:
        m = mmap.mmap(fo.fileno(),0,prot=mmap.PROT_READ)
        read = m.readline()
        result = read.split(" ")
    end = time()
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
