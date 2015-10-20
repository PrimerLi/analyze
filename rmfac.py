import os

Test_run = []
for i in range(1, 21):
    Test_run.append("Test_run" + str(i))

work = os.getcwd()
for i in range(len(Test_run)):
    os.chdir(Test_run[i])
    if (os.path.exists("sig_fac")):
	os.system("rm sig_fac")
    os.chdir("../")
