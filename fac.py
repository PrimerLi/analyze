import os
import sys
import numpy

ifile = open("param_CDMFT", 'r')
for (index, string) in enumerate(ifile):
    if (index == 7):
	a = string.replace(",", "").split()
	i_mix = int(a[3])
	if (not (i_mix == 1)):
	    sys.exit(-1)
    if (index == 8):
	string = string.replace(",", "")
	a = string.split()
	sig_fac = float(a[0])
	mu_fac = float(a[1])
    elif(index == 9):
    	a = string.replace(",", "").split()
	iter = int(a[1])
	Niter = int(a[2])
	break
ifile.close()

if(os.path.exists("../Test_run" + str(iter - 1))):
    if (os.path.exists("../Test_run" + str(iter - 1) + "/sig_fac_new")):
	os.system("cp ../Test_run" + str(iter - 1) + "/sig_fac_new sig_fac_old")

if (os.path.exists("sig_fac_old")):
    ifile = open("sig_fac_old", "r")
    for (index, string) in enumerate(ifile):
	sig_fac = float(string)
	mu_fac = sig_fac
    ifile.close()

if(not os.path.exists("Niom")):
    print "Niom does not exist. "
    sys.exit(-1)

ifile = open("Niom", "r")
for (index, string) in enumerate(ifile):
    if (index == 0):
	Niom = int(string)
    elif(index == 1):
	Niom2 = int(string)
ifile.close()

if (iter >= 3):
    dsigma1 = 0
    dsigma2 = 0
    current = os.getcwd()
    os.chdir("../Test_run" + str(iter - 2))
    if (iter - 2 == 1):
	inputFile = "Self_energy_original"
	ifile = open(inputFile, "r")
	for (index, string) in enumerate(ifile):
	    if (index == 1):
		a = string.split()
		sigma1_real = float(a[1])
	    elif(index == 2):
		sigma1_imag = float(string)
		break
	ifile.close()
    else:
	inputFile = "Self_energy"
	ifile = open(inputFile, "r")
	for (index, string) in enumerate(ifile):
	    if (index == 1):
		a = string.split()
		sigma1_real = float(a[1])
		sigma1_imag = float(a[2])
		break
	ifile.close()
    sigma1 = numpy.sqrt(sigma1_real**2 + sigma1_imag**2)

    os.chdir("../Test_run" + str(iter - 1))
    ifile = open("Self_energy", "r")
    for (index, string) in enumerate(ifile):
	if (index == 1):
	    a = string.split()
	    sigma2_real = float(a[1])
	    sigma2_imag = float(a[2])
	    break
    ifile.close()
    sigma2 = numpy.sqrt(sigma2_real**2 + sigma2_imag**2)
    
    os.chdir("../Test_run" + str(iter))
    ifile = open("Self_energy", "r")
    for (index, string) in enumerate(ifile):
	if (index == 1):
	    a = string.split()
	    sigma3_real = float(a[1])
	    sigma3_imag = float(a[2])
	    break
    ifile.close()
    sigma3 = numpy.sqrt(sigma3_real**2 + sigma3_imag**2)

    dsigma1 = sigma2 - sigma1
    dsigma2 = sigma3 - sigma2
    product = dsigma1*dsigma2
    if (product > 0):
	sig_fac = sig_fac + 0.5*sig_fac
	if (sig_fac > 0.9):
	    sig_fac = 0.9
    else:
        sig_fac = sig_fac - 0.5*sig_fac
     	if (sig_fac < 0.1):
	    sig_fac = 0.1

    ofile = open("sig_fac_new", "w")
    ofile.write(str(sig_fac))
    ofile.close()
