from writeOnFiles import writeText
from misc import sanitize

import numpy as np

#@graph is the graph (matrix) to be displayed
#@graph[i][j] = (name of sample i, name of sample j, delta, distance between i and j)
#and delta = 1 if there is an edge between i and j, otherwise 0.
#All these functions write a DOT code in file

#For non-oriented graphs
def graphNO(graph):
    filename = sanitize(raw_input("In which file do you want to store it?"))
    data = "graph g { \n"
    n,m = np.shape(graph)
    for i in range(n):
        for j in range(i+1,m):
            namei,namej,delta,distance = graph[i][j]
            if delta:
                data += "%s -- %s [label=%s]; \n"%(namei,namej,str(distance))
    data += " } \n"
    writeOnFiles(filename,data)
