
from __future__ import division
import os
def fun(x):
    return {
         1: 'rr.tr',
         2: 'nrr.tr',
	 3: 'vv.tr',
	 4: 'nrv.tr',
    }.get(x, 'null') 

def tp_flow1(fn):
	with open(fn) as f:
		thr1 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr1+= int(params[5])
		thrmbps = (thr1*8)/10000
		return str(float("{0:.2f}".format(thrmbps)))

def tp_flow2(fn):
	with open(fn) as f:
		thr2 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[2] == '2' and params[3] == '5' and params[4] == 'tcp':
				thr2+= int(params[5])
		thrmbps = (thr2*8)/10000
		return str(float("{0:.2f}".format(thrmbps)))

def filewrite(ln):
	with open('tpfairness.txt','a') as f:
		f.write(ln)
		f.close()	
if os.path.isfile('tpfairness.txt'):
	os.remove('tpfairness.txt')
for x in range(1,11):
	filename='out'
	filename+=str(x)
	line=''
	for y in range(1,5):
		line+=tp_flow1(filename+fun(y))+'\t'
		line+=tp_flow2(filename+fun(y))+'\t'
	filewrite(line+'\n')

		
			
