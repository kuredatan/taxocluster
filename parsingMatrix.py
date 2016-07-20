import numpy as np

#For distance matrices in folder /files
#Stores the results in a dictionary
#dataArray[3] = filenames
def importMatrixToDict(filename,dataArray):
    file_matrix = open("meta/" + filename + ".dist","r")
    lines = file_matrix.readlines()[3:-3]
    file_matrix.close()
    n = len(lines)
    m = len(lines[0].split(" | "))
    ln = len(filenames)
    values = []
    for i in range(ln):
        for j in range(i+1,ln):
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
    
