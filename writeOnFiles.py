import numpy as np

def writeText(filename,data):
    try:
        fo = open("files/" + filename + ".taxocluster","w")
        fo.write(data)
        fo.close()
    except IOError:
        print "\n/!\ ERROR: Could not open the file. Please try another name."
        raise ValueError

def writeArray(filename,data,header):
    np.savetxt("files/" + filename + ".taxocluster",data,"%s"," | "," \n",header + " \n","\n\nEND OF FILE ****","")

def writeMatrix(filename,data,header):
    np.savetxt("meta/" + filename + ".dist",data,"%s"," | "," \n",header + " \n","\n\nEND OF FILE ****","")

def writeDot(filename,data):
    try:
        fo = open("files/" + filename + ".dot","w")
        fo.write(data)
        fo.close()
    except IOError:
        print "\n/!\ ERROR: Could not open the file. Please try another name."
        raise ValueError

def writeFile(data,header="",typeData="text"):
    filename = raw_input("In which file do you want to write it? [Be careful not to choose a name that already exists as it would truncate the existing file]\n")
    if (typeData == "text"):
        writeText(filename,data)
    elif (typeData == "array"):
       	writeArray(filename,data,header)
    elif (typeData == "matrix"):
        writeMatrix(filename,data,header)
    elif (typeData == "dot"):
        writeDot(filename,data)
    else:
        print "\n/!\ ERROR: Unknown type of data."
        raise ValueError
    print "-- End of writing\n"

