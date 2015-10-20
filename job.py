import os
import sys

if (len(sys.argv) != 3):
    print "hour = sys.argv[1], nodes = sys.argv[2]. "
    sys.exit(-1)

hour = int(sys.argv[1])
nodes = int(sys.argv[2])

os.system("qsub -I -l walltime=" + str(hour) + ":00:00,nodes=" + str(nodes) + ":ppn=20 -A loni_dca_14")
