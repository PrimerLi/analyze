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

work = "/work/enzhili"

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
	    #shutil.copyfile("../readmu.py", "./readmu.py")
	    #execfile("readmu.py")
	    #os.chdir(currentDirectory)
	    #os.chdir("./mu")
	    #shutil.copyfile("fill", work + "/Chi/" + destination + "/fill_" + beta[ibeta])
	    #os.chdir("../")
	    if (os.path.exists("./mu")):
		pass
	    else:
	        os.system("../readmu.py .")
	 	os.system("python readmu.py")
	 	os.chdir(currentDirectory)
	    os.chdir("./mu")
	    os.system("cp chem " + work + "/Chi/" + destination + "/chem_" + beta[ibeta])
	    os.chdir("..")
	    folders = os.listdir(".")
	    count_Test_run = 0
	    for folder in folders:
	        if ("Test_run" in folder):
		    count_Test_run = count_Test_run + 1
	    final = "Test_run" + str(max(iterationMax, count_Test_run))
	    if (os.path.exists(final)):
		os.chdir(final)
		if (os.path.exists("Chi_int")):
		    os.system("cp Chi_int " + work + "/Chi/" + destination + "/Chi_int_" + beta[ibeta])
		    if (os.path.exists("M.txt")):
			os.system("cp ../../eigenvalues/eigenvalues.out .")
			os.system("cp ../../eigenvalues/pre.py .")
			if (not (os.path.exists("M_regularized"))):
			    os.system("python pre.py M.txt")
			if (not (os.path.exists("eigenvalues.txt"))):
			    os.system("./eigenvalues.out")
			os.system("cp eigenvalues.txt" + "  " + work + "/Chi/" + destination + "/eigenvalues_" + beta[ibeta])
			os.system("rm eigenvalues.out")
		    if (os.path.exists("Chi_int_charge")):
			os.system("cp Chi_int_charge" + "  " + work + "/Chi/" + destination + "/Chi_int_charge_" + beta[ibeta])
	    os.chdir(work)
	else:
	    print directory + " not found "
