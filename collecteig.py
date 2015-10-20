import os 
import shutil
import sys

V = 0.8
U = 4 
gc = 1
beta = []
fill = 1.8
Niom_factor = 5
Niom2_factor = 2
shift = 0
Om = 0.01 
iterationMax = 20

if (os.path.exists("beta")):
    ifile = open("beta", 'r')
    for (index, string) in enumerate(ifile):
	b = string.replace("\n", "")
	beta.append(b)	
    ifile.close()
else:
    print "beta does not exist. "
    sys.exit(-1)

work = os.getcwd()

if (not os.path.exists("Chi")):
    os.mkdir("Chi")

if (os.path.exists("Chi")):
    os.chdir("./Chi")
    destination = "V" + "%.1f"%V + "Uhub" + str(U) + "gc" + str(gc) + "Niom_" + str(Niom_factor) + "Niom2_" + str(Niom2_factor) + "fill_" + str(fill) + "Om_" + str(Om)
    if (os.path.exists(destination)):
	pass
    else:
    	os.mkdir(destination)
    os.chdir(work)

os.chdir(work)

count = 0
for ibeta in range(len(beta)):
	count = count + 1
	directory = "V_" + "%.1f"%V + "Uhub_" + str(U) + "gc_" + str(gc) + "beta_" + beta[ibeta] + "fill_" + str(fill) + "Om_" + str(Om) + "Niom_" + str(Niom_factor) + "Niom2_" + str(Niom2_factor) + "n_" + str(count + shift);
	print beta[ibeta]
	if (os.path.exists(directory)):
	    os.chdir(directory)
	    currentDirectory = os.getcwd()
	    final = "Test_run" + str(iterationMax)
	    if (os.path.exists(final)):
		os.chdir(final)
		if (os.path.exists("Chi_int")):
		    if (os.path.exists("M.txt")):
			#os.system("cp ../../eigenvalues/eigenvalues.out .")
			#os.system("cp ../../eigenvalues/pre.py .")
			#os.system("python pre.py M.txt")
			#os.system("eigenvalues.out ")
			#os.system("cp eigenvalues.txt" + "  " + work + "/Chi/" + destination + "/eigenvalues_" + beta[ibeta])
			os.system("cp rightEigenvectors.txt" + "  " + work + "/Chi/" + destination + "/rightEigenvectors_" + beta[ibeta])
			#os.system("rm eigenvalues.out")
	    os.chdir(work)
	else:
	    print directory + " not found "
