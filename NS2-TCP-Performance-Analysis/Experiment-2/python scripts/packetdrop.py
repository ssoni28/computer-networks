import os
def fun(x):
    return {
         1: 'rr.tr',
         2: 'nrr.tr',
	 3: 'vv.tr',
	 4: 'nrv.tr',
    }.get(x, 'null') 

def drop_flow1(fn):
	with open(fn) as f:
		d1 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'd' and params[8] == '0.0' and params[9] == '3.0' and params[4] == 'tcp':
				d1+= 1
		return str(d1)

def drop_flow2(fn):
	with open(fn) as f:
		d2 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'd' and params[8] == '4.0' and params[9] == '5.0' and params[4] == 'tcp':
				d2+= 1
		return str(d2)

def drop_cbr(fn):
	with open(fn) as f:
		d3 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'd' and params[8] == '1.0' and params[9] == '2.0' and params[4] == 'cbr':
				d3+= 1
		return str(d3)

def filewrite(ln):
	with open('dropfairness.txt','a') as f:
		f.write(ln)
		f.close()	
if os.path.isfile('dropfairness.txt'):
	os.remove('dropfairness.txt')
for x in range(1,11):
	filename='out'
	filename+=str(x)
	line=''
	for y in range(1,5):
		line+=drop_flow1(filename+fun(y))+'\t'
		line+=drop_flow2(filename+fun(y))+'\t'
		line+=drop_cbr(filename+fun(y))+'\t'
	filewrite(line+'\n')

		
			
