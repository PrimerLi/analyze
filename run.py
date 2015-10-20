import os

Test_run = []
for i in range(1, 21):
    Test_run.append("Test_run" + str(i))

work = os.getcwd()
os.system("python rmfac.py")
os.chdir(work)
for i in range(len(Test_run)):
    os.chdir(Test_run[i])
    os.system("cp ../fac.py .")
    os.system("python fac.py ")
    os.chdir("../")
