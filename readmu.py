import os
import shutil
import sys

def getDigit(parameter):
    a = []
    for element in parameter:
    	if element.isdigit():
	    a.append(element)
    string = ""
    for digit in a:
        string = string + digit
    return string

folders = os.listdir(".")
TestRun = []
for folder in folders:
	if ("Test_run" in folder):
	    TestRun.append(folder)

if (os.path.exists("mu")):
    pass
else:
    os.mkdir("mu")

for folder in TestRun:
    if (not os.path.exists("./" + folder)):
        print os.getcwd()
        continue 
    os.chdir("./" + folder)
    if (os.path.exists("mu_fill")):
        shutil.copyfile("./mu_fill", "../mu/mu_fill_" + getDigit(folder))
        if (os.path.exists("betaInfo")):
            os.system("cp betaInfo ../mu/")
        os.chdir("../")
    else:
        os.chdir("../")

os.chdir("./mu")
files = os.listdir(".")
mu_fill = []
for file in files:
	if ("mu_fill" in file):
	    mu_fill.append(file)
	
result = []
for file in mu_fill:
	ifile = open(file, 'r')
	for (index, string) in enumerate(ifile):
	    if (index == 0):
		a = string.split()
		result.append(getDigit(file) + "    " + a[1])
		break
	ifile.close()

for i in range(len(result)):
    min = result[i]
    for j in range(i, len(result)):
	if (int(result[j].split()[0]) < int(min.split()[0])):
	    temp = min
	    min = result[j]
	    result[j] = temp
    result[i] = min

ofile = open("fill", 'w')
for i in range(len(result)):
    ofile.write(result[i] + "\n")
ofile.close()
