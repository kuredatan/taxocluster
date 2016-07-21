import sys as s
import subprocess as sb
from time import time

from parsingInfo import parseInfo
from taxoTree import TaxoTree
from actions import clusteringAct,printTreeAct,parseList
from featuresVector import featuresCreate
from preformat import process
from misc import mergeList
from computeDistances import computeDistanceMatrix,distMatched,distConsensus
from importMatrix import importMatrixToDict

#/!\ The list of samples ID is supposed to be the same as the list of .match files! Each .match file must correspond to one single sample!
def main():
    iMatrix = raw_input("Write down the CSV file name of the data matrix in the folder \"meta\" [ without the extension .csv ]\n")
    if (iMatrix == ""):
        iMatrix = "Info"
    fastaFileName = raw_input("Write down the FASTA file name in the folder \"meta\" [ without the extension .fasta ]\n")
    if (fastaFileName == ""):
        fastaFileName = "GREENGENES_gg16S_unaligned_10022015"
    print "/!\ Data getting parsed..."
    try:
        samplesInfoList,infoList = parseInfo(iMatrix)
        filenames = [sample[0] for sample in samplesInfoList]
    except IOError:
        print "\nERROR: Maybe the filename",iMatrix,".csv does not exist in \"meta\" folder.\n"
        s.exit(0)
    print "-- End of parsing\n"
    result = sb.check_output("ls ./meta/match/testfiles",shell=True)
    sb.call("ls ./meta/match > sampleidlist",shell=True)
    sampleidlist = sb.check_output("sed 's/.match//g' sampleidlist | sed 's/testfiles//g' | sed '/^$/d'",shell=True).split()
    sb.call("rm -f sampleidlist",shell=True)
    if not result:
        print "/!\ Pre-processing files for parsing..."
        process(sampleidlist)
        print "/!\ Pre-processing done."
    print "/!\ Constructing the features vectors..."
    sampleList = mergeList(sampleidlist,filenames)
    try:
        matchingNodes,idSequences,paths,nodesListTree = featuresCreate(sampleList,fastaFileName)
    except ValueError: 
        print "/!\ ERROR: Please look at the line above."
        print "/!\ ERROR: If the line above is blank, it may be an uncatched ValueError.\n"
        s.exit(0)
    print "-- End of construction"
    print "/!\ Constructing the whole taxonomic tree..."
    print "[ You may have to wait a few seconds... ]"
    taxoTree = TaxoTree("Root").addNode(paths,nodesListTree)
    print "-- End of construction\n"
    dataArray = [samplesInfoList,infoList,idSequences,sampleList,matchingNodes,paths,nodesListTree,taxoTree]
    filesList = sb.check_output("ls ./meta | awk '/.dist/'",shell=True).split()
    if not filesList:
        print "/!\ Computing distance matrix... (1/2)"
        start = time()
        computeDistanceMatrix(distMatched,dataArray)
        end = time()
        print "TIME:",end-start,"sec"
        print "/!\ Computing distance matrix... (2/2)"
        start = time()
        computeDistanceMatrix(distConsensus,dataArray)
        end = time()
        print "TIME:",end-start,"sec"
        print "-- End of computation."
    answer = None
    done = False
    while not done and not (answer == "exit" or answer == "exit()" or answer == "quit" or answer == "quit()"):
        try:
            answer = raw_input("Do you want to compute distance matrix for another value of q or import pre-computed matrices? compute/import\n")
            if answer == "compute":
                print "/!\ Computing distance matrix..."
                start = time()
                computeDistanceMatrix(distConsensus,dataArray)
                end = time()
                print "TIME:",end-start,"sec"
                print "-- End of computation."
                done = True
            elif not (answer == "import"):
                print "\n/!\ You should answer by 'compute' or 'import'!"
                raise ValueError
            done = True
            undone = True
            while undone:
                qList = sorted(sb.check_output("ls ./meta | awk '/.dist/' | sed 's/matrix[1-2]//g' | sed 's/.dist//g'",shell=True).split())
                print "List of pre-computed q:",qList
                q = raw_input("Choose q among the ones above.\n")
                if float(q) < 0 or float(q) > 1:
                    print "\n/!\ ERROR: Wrong value of q [should be between 0 and 1, and be already computed]:",q,"."
                    continue
                else:
                    undone = False
            distMatchedDict = importMatrixToDict("matrix1",dataArray)
            distConsensusDict = importMatrixToDict("matrix2" + q,dataArray)
            dataArray.append(distMatchedDict)
            dataArray.append(distConsensusDict)
            print "/!\ Matrices imported."
        except ValueError:
            continue
    answer = ""
    while not ((answer == "exit") or (answer == "exit()") or (answer == "quit") or (answer == "quit()")):
        try:
            print "What do you want to do?"
            print "[Write down the number matching with the action required. Details are in README file]"
            print "   1: Clustering"
            print "   2: Print the taxonomic tree"
            print "[To quit, write down exit]"
            answer = raw_input("Your answer?\n")
            if (answer =="1"):
                clusteringAct(dataArray)
                print "-- End \n"
            elif (answer == "2"):
                printTreeAct(dataArray)
                print "-- End \n"
            elif not ((answer == "exit") or (answer == "exit()") or (answer == "quit")):
                print "/!\ ERROR: Please enter a number between 1 and 2 included, or 'exit' if you want to quit."
                raise ValueError
        except ValueError:
            print "/!\ ERROR: Please look at the line above."
            print "/!\ ERROR: If the line above is blank, it may be an uncatched ValueError.\n"   
