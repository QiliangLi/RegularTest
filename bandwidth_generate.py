from scipy.stats import zipf
import os
from os.path import dirname
import numpy
from random import shuffle
'''
'''

def bandwidth_generate(maxbandwith = 125,maxrate = 0.99, numofnode = 16, turn = 2): #size in MB

	a = 1.0000001 #the exponent of zipf, a > 1.

	listofoutput = [] #save the bandwidth
	for i in range(1, numofnode+1 ,1):
		tmp = zipf.pmf(i,a) / zipf.pmf(1,a) * maxbandwith * maxrate #generate
		listofoutput.append( int(tmp) )
	print(listofoutput)

	fw_used = open("bandwidth_used.txt", "w")
	fw_rest = open("bandwidth_rest.txt", "w")

	for i in range(1, turn+1, 1): #output
		shuffle(listofoutput)     #random
		for j in range(0, numofnode-1 ,1):
			fw_used.write("%d " % listofoutput[j])
			fw_rest.write("%d " % (maxbandwith - listofoutput[j]) )
		fw_used.write("%d\n" % listofoutput[-1])
		fw_rest.write("%d\n" % (maxbandwith - listofoutput[-1]) )

	fw_used.close()
	fw_rest.close()

if __name__ == "__main__":
	bandwidth_generate()
    #bandwidth_generate(int(sys.argv[1]), float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))