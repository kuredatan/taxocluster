import sys as s
import subprocess as sb

from parsingInfo import parseInfo
from parsingTree import parseTree
from taxoTree import TaxoTree
from actions import clusteringAct,printTreeAct,parseList
from featuresVector import featuresCreate
from preformat import process

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
        filenames = sorted([sample[0] for sample in samplesInfoList],lambda x:x)
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
        process(filenames)
        print "/!\ Pre-processing done."
    print "/!\ Constructing the whole taxonomic tree..."
    taxoTree = TaxoTree("Root").addNode(paths,nodesListTree)
    print "/!\ Constructing the features vectors..."
    try:
        matchingNodes,idSequences = featuresCreate(filenames,fastaFileName)
    except ValueError:
        print "/!\ ERROR: Please look at the line above."
        print "/!\ ERROR: If the line above is blank, it may be an uncatched ValueError.\n"
        s.exit(0)
    print "-- End of construction\n"
    dataArray = [samplesInfoList,infoList,idSequences,filenames,matchingNodes,paths,nodesListTree,taxoTree]
    answer = ""
    while not ((answer == "exit") or (answer == "exit()") or (answer == "quit")):
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
