import os

fill = []
filling = []
Test_run = []

work = os.getcwd()

if (os.path.exists("fill")):
    pass
else:
    os.mkdir("fill")

for i in range(1, 21):
    Test_run.append("Test_run" + str(i))

for i in range(len(Test_run)):
    if (os.path.exists("./" + Test_run[i])):
	os.chdir("./" + Test_run[i])
	os.system("cp fill ../fill/fill_" + str(i + 1))
	os.chdir(work)

os.chdir(work)
os.chdir("fill")
for i in range(1, 21):
    fill.append("fill_" + str(i))

for i in range(len(fill)):
    if (os.path.exists(fill[i])):
	ifile = open(fill[i], "r")
	for (index, string) in enumerate(ifile):
	    if (index == 0):
		a = string.split()
		filling.append(a[0])
		break
	ifile.close()

ofile = open("fill.txt", "w")
for i in range(len(filling)):
    ofile.write(str(i + 1) + "     " + str(filling[i]) + "\n")
ofile.close()
