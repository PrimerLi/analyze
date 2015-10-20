import os
import sys

iterationMax = 0
tail = 0
chem = []
eps_f = []
i_fix = 0

ifile = open("betaInfo", "r")
for (index, string) in enumerate(ifile):
    if (index == 1):
	i_fix = int(string.replace("\n", ""))
ifile.close()

files = os.listdir(".")
mu_fill = []
for file in files:
	if ("mu_fill_" in file):
	    mu_fill.append(file)

iterationMax = len(mu_fill)
tail = int(1.0*iterationMax)

for i in range(iterationMax):
	ifile = open("mu_fill_" + str(i+1), "r")
	for (index, string) in enumerate(ifile):
	    if (index == 0):
		a = string.split()
		chem.append(float(a[0]))
	    elif (index == 2):
		a = string.split()
		eps_f.append(float(a[0]))

sum = 0
average = 0
count = 0
ofile = open("chem", "w")
for ele in chem:
    count = count + 1
    ofile.write(str(count) + "    " + str(ele) + "\n")
    sum = sum + ele
ofile.close()

sum = 0
average = 0
count = 0
ofile = open("eps_f", "w")
for ele in eps_f:
    count = count + 1
    ofile.write(str(count) + "   " + str(ele) + "\n")
    sum = sum + ele
ofile.close()

sum = 0
samplesize = 3
average = 0
for i in range(samplesize):
    sum = sum + chem[iterationMax - i - 1]
average = sum/samplesize
ofile = open("average", "w")
if (i_fix == 0):
    ofile.write(str(average))
else:
    ofile.write(str(average) + "   " + str(eps_f[len(eps_f) - 1]))
ofile.close()
