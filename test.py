from time import time 
import mmap
    
def readIt(filename):
    start = time()
    with open(filename,"r+b") as fo:
        m = mmap.mmap(fo.fileno(),0,prot=mmap.PROT_READ)
        #r = fo.readlines()
        r = fo.xreadlines()
        #line = m.readline()
        #while line:
        for line in r:
            n = len(line)
            for _ in range(n):
                ()
            #line = m.readline()
    end = time()
    print (end-start)

def getPathMatch(filename):
    return "meta/match/" + filename + ".match"

def getPathFasta(filename):
    return "meta/" + filename + ".fasta"

def test(filename,fasta=False):
    if fasta:
        readIt(getPathFasta(filename))
    else:
        readIt(getPathMatch(filename))

def testList(filesList):
    start = time()
    foList = []
    for filename in filesList:
        try:
            foList.append(open(getPathMatch(filename),"r+b"))
        except IOError:
            continue
    i = 0
    for filename in filesList:
        print filename
            #with open(getPathMatch(filename),"r+b") as fo:
        try:
            m = mmap.mmap(foList[i].fileno(),0,prot=mmap.PROT_READ)
                #r = fo.readlines()
                #r = fo.xreadlines()
                #line = m.readline()
                #while line:
            for line in foList[i]:
                n = len(line)
                for _ in range(n):
                    ()
                    #line = m.readline()
            foList[i].close()
        except IndexError:
            continue
        i += 1
    for fo in foList:
        fo.close()
    end = time()
    print (end-start),i
        
def testOnlyFasta():
    test("GREENGENES_gg16S_unaligned_10022015",True)

def benchmark():
    from parsingInfo import parseInfo
    samplesList,_ = parseInfo("Info")
    samplesIDList = [sample[0] for sample in samplesList]
    testList(samplesIDList)
