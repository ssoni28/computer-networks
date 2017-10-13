from __future__ import division
import os
def fun(x):
    return {
         1: 'reno_droptail_out.tr',
         2: 'reno_red_out.tr',
	 3: 'sack_droptail_out.tr',
	 4: 'sack_Red_out.tr',
    }.get(x, 'null') 

def tp_flow1(fn):
	with open(fn) as f:
		thr1 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] <= '1.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr1+= int(params[5])
                thrKbps = ((thr1 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow2(fn):
	with open(fn) as f:
		thr2 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] > '1.0' and params[1] <= '2.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr2+= int(params[5])
		thrKbps = ((thr2 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow3(fn):
	with open(fn) as f:
		thr3 = 0
		for line in f:
			params= line.split( )	 
			if params[0] == 'r' and params[1] > '2.0' and params[1] <= '3.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr3+= int(params[5])
		thrKbps = ((thr3 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow4(fn):
	with open(fn) as f:
		thr4 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] > '3.0' and params[1] <= '4.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr4+= int(params[5])
		thrKbps = ((thr4 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow5(fn):
	with open(fn) as f:
		thr5 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] > '4.0' and params[1] <= '5.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr5+= int(params[5])
		thrKbps = ((thr5 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow6(fn):
	with open(fn) as f:
		thr6 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] > '5.0' and params[1] <= '6.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr6+= int(params[5])
		thrKbps = ((thr6 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow7(fn):
	with open(fn) as f:
		thr7 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] > '6.0' and params[1] <= '7.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr7+= int(params[5])
		thrKbps = ((thr7 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow8(fn):
	with open(fn) as f:
		thr8 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] > '7.0' and params[1] <= '8.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr8+= int(params[5])
		thrKbps = ((thr8 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow9(fn):
	with open(fn) as f:
		thr9 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] > '8.0' and params[1] <= '9.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr9+= int(params[5])
		thrKbps = ((thr9 * 8)/1000)
		return str(round(thrKbps,4))

def tp_flow10(fn):
	with open(fn) as f:
		thr10 = 0
		for line in f:
			params= line.split( )	
			if params[0] == 'r' and params[1] > '9.0' and params[1] <= '10.0' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':
				thr10+= int(params[5])
		thrKbps = ((thr10 * 8)/1000)
		return str(round(thrKbps,4))


def filewrite(ln):
	with open('renodroptail.txt','a') as f:
		f.write(ln)
		f.close()	
if os.path.isfile('renodroptail.txt'):
	os.remove('renodroptail.txt')
for x in range(1,5):
        line=''
        line+=tp_flow1(fun(x))+'\t'
        line+=tp_flow2(fun(x))+'\t'
        line+=tp_flow3(fun(x))+'\t'
        line+=tp_flow4(fun(x))+'\t'
        line+=tp_flow5(fun(x))+'\t'
        line+=tp_flow6(fun(x))+'\t'
        line+=tp_flow7(fun(x))+'\t'
        line+=tp_flow8(fun(x))+'\t'
        line+=tp_flow9(fun(x))+'\t'
        line+=tp_flow10(fun(x))+'\t'
        filewrite(line+'\n')
	
	

			

