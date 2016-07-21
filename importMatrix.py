import numpy as np
import sys as s
import re

#For distance matrices in folder /files
#Stores the results in a dictionary
#dataArray[3] = filenames
def importMatrixToDict(filename,dataArray):
    try:
        file_matrix = open("meta/" + filename + ".dist","r")
    except IOError:
        print "\n/!\ ERROR: Wrong file name",filename,". Maybe this file does not exist."
        s.exit(0)
    lines = file_matrix.readlines()[3:-3]
    file_matrix.close()
    n = min(len(dataArray[3]),len(lines))
    values = []
    for i in range(n):
        for j in range(i,n):
            values.append((dataArray[3][i],dataArray[3][j]))
            values.append((dataArray[3][j],dataArray[3][i]))
    #Initializing the dictionary
    distDict = dict.fromkeys(values)
    for i in range(n):
        currRow = lines[i]
        #Reversing the list
        columns = currRow.split(" | ")[::-1]
        j = 0
        while columns:
            currCol = columns.pop()
            distDict[(dataArray[3][i],dataArray[3][j])] = float(currCol)
            distDict[(dataArray[3][j],dataArray[3][i])] = float(currCol)
            j += 1
    return distDict
    
