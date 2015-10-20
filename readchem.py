import os
import sys

def getdigit(fileName):
    string = ""
    for i in range(len(fileName)):
	if (fileName[i].isdigit()):
	    for j in range(i, len(fileName)):
		string = string + fileName[j]
	    break
    return string

beta = []
files = os.listdir(".")
for file in files:
    if ("chem_" in file):
	beta.append(getdigit(file))

def numeric(a, b):
    if (float(a) > float(b)):
	return 1
    elif(float(a) < float(b)):
	return -1
    else:
        return 0

beta = sorted(beta, cmp = numeric)

chem = []

for i in range(len(beta)):
    fileName = "chem_" + beta[i]
    if (os.path.exists(fileName)):
	ifile = open(fileName, "r")
	for (index, string) in enumerate(ifile):
	    linenumber = index
	ifile.close()
	ifile = open(fileName, "r")
	for (index, string) in enumerate(ifile):
	    if (index == linenumber):
		chem.append(string.split()[1])
	ifile.close()

ofile = open("mu_beta", "w")
for i in range(len(chem)):
    ofile.write(beta[i] + "    " + chem[i] + "\n")
ofile.close()

for i in range(len(chem)):
    print str(1.0/float(beta[i])) + "    " + chem[i]
