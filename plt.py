import sys
import matplotlib.pyplot as plt

if(len(sys.argv)!=2):
    sys.exit("argv[1]==fileName")

x=[]
y=[]

fileName=sys.argv[1]

try:
    ifile=open(fileName)
except:
    sys.exit(fileName+" does not exist. ")

for index, string in enumerate(ifile):
    a=string.split()
    x.append(float(a[0]))
    y.append(float(a[1]))
ifile.close()
    
lowerY=0
if(min(y)<0):
    lowerY=min(y)

upperY = max(y)
if (max(y) < 0):
    upperY = 0

plt.plot(x, y)
plt.xlim([min(x), max(x)])
plt.ylim([1.1*lowerY, 1.2*upperY])
plt.grid()
plt.show()
