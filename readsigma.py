import os

folders = os.listdir(".")
count = 0
for folder in folders:
	if ("Test_run" in folder):
	    count = count + 1

Test_run = []
for i in range(1, count + 1):
    Test_run.append("Test_run" + str(i))

work = os.getcwd()
sigma_real = []
sigma_imag = []
sig_fac = []

for i in range(len(Test_run)):
    if (not os.path.exists("./" + Test_run[i])):
	continue
    os.chdir("./" + Test_run[i])
    if (os.path.exists("sig_fac_new")):
	ifile = open("sig_fac_new", "r")
	for (index, string) in enumerate(ifile):
	    sig_fac.append(string)
	ifile.close()
    if (os.path.exists("Self_energy")):
	ifile = open("Self_energy", "r")
	for (index, string) in enumerate(ifile):
	    if (index == 1):
		a = string.split()
		sigma_real.append(a[1])
		sigma_imag.append(a[2])
		break
	ifile.close()
    elif(os.path.exists("Self_energy_original")):
	ifile = open("Self_energy_original", "r")
	for (index, string) in enumerate(ifile):
	    if(index == 1):
		a = string.split()
		sigma_real.append(a[1])
	    elif(index == 2):
		sigma_imag.append(string.replace("\n", ""))
	ifile.close()
    else:
	print "Self_energy cannot be opened. "
	print os.getcwd()
    os.chdir("../")

real = open("Self_energy_real", "w")
imag = open("Self_energy_imag", "w")
for i in range(len(sigma_real)):
    real.write(str(i + 1) + "     " + sigma_real[i] + "\n")
    imag.write(str(i + 1) + "     " + sigma_imag[i] + "\n")
real.close()
imag.close()

ofile = open("sig_fac.txt", "w")
for i in range(len(sig_fac)):
    ofile.write(str(i + 3) + "    " + sig_fac[i] + "\n")
ofile.close()
