from time import time
import sys as s
import re
import subprocess as sb
import numpy as np
import array

integer = re.compile("[0-9]+")

#Returns the pair (identifier of patient a.k.a. @filename,list of identifiers of sequences matching a read in this patient)
def parseMatch(filename,i):
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
    return result

#Returns dictionary @allMatches (key=sample ID a.k.a. @filename,value=list of identifiers of sequences matching a read in this sample) 
def parseAllMatch(filenames):
    allMatches = dict.fromkeys(filenames)
    i = 0
    for filename in filenames:
        try:
            if filename:
                sequencesArray = parseMatch(filename,i)
                allMatches[filename] = sequencesArray
                i += 1
        except IOError:
            print "\nERROR: Maybe the filename",filename,".match does not exist in \"meta/matches\" folder\n"
            s.exit(0)
    return allMatches

def parseAllFact(filenames):
    ln = len(filenames)
    fact = ln/12
    allMatchesList = []
    start = 0
    end = ln/fact
    for i in range(fact):
        allMatchesList.append(parseAllMatch(filenames[start:end]))
        start = end
        end += ln/fact
    allMatchesList.append(parseAllMatch(filenames[end:]))
    for matchDict in allMatchesList[1:]:
        allMatchesList[0].update(matchDict)
    return allMatchesList[0]
