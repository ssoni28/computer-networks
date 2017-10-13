from __future__ import division
import os


def fun(x):
    return {
         1: 'tahoe.tr',
         2: 'reno.tr',
	 3: 'newreno.tr',
	 4: 'vegas.tr',
    }.get(x, 'null') 

def throughput(fn):
	with open(fn) as f:
		thr1 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr1+= 1040		
		thrmbps = (thr1*8)/10000
		return str(round(thrmbps,2))
def filewrite(ln):
	with open('tpresult.txt','a') as f:
		f.write(ln)
		f.close()	
if os.path.isfile('tpresult.txt'):
	os.remove('tpresult.txt')
for x in range(1,11):
	filename='out'
	filename+=str(x)
	line=''
	for y in range(1,5):
		line+=throughput(filename+fun(y))+'\t'
	filewrite(line+'\n')

		
			

