import sys as s
import subprocess as sb

from parsingInfo import parseInfo
from parsingTree import parseTree
from taxoTree import TaxoTree
from actions import clusteringAct,printTreeAct,parseList
from featuresVector import featuresCreate
from preformat import process
from misc import mergeList
from computeDistances import computeDistanceMatrix,dist1,dist2
from importMatrix import importMatrixToDict

#/!\ The list of samples ID is supposed to be the same as the list of .match files! Each .match file must correspond to one single sample!
def main():
    tTree = raw_input("Write down the .tree file name of the taxonomic tree in the folder \"meta\" [ without the extension .tree ]\n")
    if (tTree == ""):
        tTree = "GGdb2015"
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
    print "..."
    try:
        paths,n,nodesListTree = parseTree(tTree)
    except IOError:
        print "\nERROR: Maybe the filename",tTree,".tree does not exist in \"meta\" folder.\n"
        s.exit(0)
    print "-- End of parsing\n"
    result = sb.check_output("ls ./meta/match/testfiles",shell=True)
    if not result:
        print "/!\ Pre-processing files for parsing..."
        process(sampleidlist)
        print "/!\ Pre-processing done."
    sb.call("ls ./meta/match > sampleidlist",shell=True)
    sampleidlist = sb.check_output("sed 's/.match//g' sampleidlist | sed 's/testfiles//g' | sed '/^$/d'",shell=True).split()
    sb.call("rm -f sampleidlist",shell=True)
    print "/!\ Constructing the whole taxonomic tree..."
    print "[ You may have to wait a few seconds... ]"
    taxoTree = TaxoTree("Root").addNode(paths,nodesListTree)
    print "/!\ Constructing the features vectors..."
    sampleList = mergeList(sampleidlist,filenames)
    try:
        matchingNodes,idSequences = featuresCreate(sampleList,fastaFileName)
    except ValueError: 
        print "/!\ ERROR: Please look at the line above."
        print "/!\ ERROR: If the line above is blank, it may be an uncatched ValueError.\n"
        s.exit(0)
    print "-- End of construction\n"
    dataArray = [samplesInfoList,infoList,idSequences,sampleList,matchingNodes,paths,nodesListTree,taxoTree]
    filesList = sb.check_output("ls ./meta | awk '/.dist/'",shell=True).split()
    if not filesList:
        print "/!\ Computing distance matrix... (1/2)"
        computeDistanceMatrix(dist1,dataArray)
        print "/!\ Computing distance matrix... (2/2)"
        computeDistanceMatrix(dist2,dataArray)
        print "-- End of computation."
    else:
        answer = None
        done = False
        while not done and not (answer == "exit" or answer == "exit()" or answer == "quit" or answer == "quit()"):
            try:
                answer = raw_input("Do you want to compute distance matrix for another value of q or import pre-computed matrices? compute/import\n")
                if answer == "compute":
                    print "/!\ Computing distance matrix..."
                    computeDistanceMatrix(dist2,dataArray)
                    print "-- End of computation."
                    filenameDist1 = raw_input("What is the file name for 'matched' distance matrix?\n")
                    filenameDist2 = raw_input("What is the file name for 'consensus' distance matrix to select?\n")
                    dist1Dict = importMatrixToDict(filenameDist1,dataArray)
                    dist2Dict = importMatrixToDict(filenameDist2,dataArray)
                    dataArray.append(dist1Dict)
                    dataArray.append(dist2Dict)
                    done = True
                elif answer == "import":
                    filenameDist1 = raw_input("What is the file name for 'matched' distance matrix?\n")
                    filenameDist2 = raw_input("What is the file name for 'consensus' distance matrix to select?\n")
                    dist1Dict = importMatrixToDict(filenameDist1,dataArray)
                    dist2Dict = importMatrixToDict(filenameDist2,dataArray)
                    dataArray.append(dist1Dict)
                    dataArray.append(dist2Dict)
                    done = True
                else:
                    print "\n/!\ You should answer by 'compute' or 'import'!"
                    raise ValueError
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
