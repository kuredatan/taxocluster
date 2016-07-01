#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes,paths,n,nodesList,taxoTree]

#distance(@sample1,@sample2) = |number of nodes matched in @sample1| + |number of nodes matched in @sample2| - 2*|number of nodes matched in both samples|
def distance1(sample1,sample2,dataArray): 
