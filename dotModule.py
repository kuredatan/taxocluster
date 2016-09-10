from writeOnFiles import writeFile
from misc import sanitize

import numpy as np

#@graph is the graph (matrix) to be displayed
#@graph[i][j] = (name of sample i, name of sample j, delta, distance between i and j)
#and delta = 1 if there is an edge between i and j, otherwise 0.
#All these functions write a DOT code in file

def sanitizeDot(name):
    newName = ""
    for letter in name:
        if not letter == "-":
            newName += letter
    return newName

#For non-oriented graphs
def graphNO(graph):
    seen = dict.fromkeys([])
    data = "graph g { \n"
    n,m = np.shape(graph)
    for i in range(n):
        for j in range(i+1,m):
            if graph[i][j]:
                namei,namej,delta,distance = graph[i][j]
                if delta and not seen.get((namei,namej)) :
                    data += "%s -- %s [label=%s]; \n"%(sanitizeDot(namei),sanitizeDot(namej),str(distance))
                    seen.setdefault((namei,namej),1)
                    seen.setdefault((namej,namej),1)
    data += " } \n"
    writeFile(data,"","dot")
    
