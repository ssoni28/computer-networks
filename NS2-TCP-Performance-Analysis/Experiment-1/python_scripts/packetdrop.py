import os        
def fun(x):
    return {
         1: 'tahoe.tr',
         2: 'reno.tr',
	 3: 'newreno.tr',
	 4: 'vegas.tr',
    }.get(x, 'null') 

def drop(fn):
	with open(fn) as f:
		drop = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'd' and params[4] == 'tcp':
				drop+= 1
		return str(drop)
def filewrite(ln):
	with open('dropresult.txt','a') as f:
		f.write(ln)
		f.close()	
if os.path.isfile('dropresult.txt'):
	os.remove('dropresult.txt')
for x in range(1,11):
	filename='out'
	filename+=str(x)
	line=''
	for y in range(1,5):
		line+=drop(filename+fun(y))+'\t'
	filewrite(line+'\n')

		
			

