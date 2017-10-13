import os
def fun(x):
    return {
         1: 'rr.tr',
         2: 'nrr.tr',
	 3: 'vv.tr',
	 4: 'nrv.tr',
    }.get(x, 'null') 

start_time_map_f1 = {};
start_time_map_f2 = {};

def st_time_map_f1(fn):
	with open(fn) as f:               
		latency_sum = 0
		packet_bytes = 0
		num_packets = 0
		global start_time_map_f1
		for line in f:			
			params= line.split( )	
			if params[0] == '+' and params[2] == '0' and params[3] == '1' and params[4] == 'tcp':				
				start_time_map_f1[params[11]] = params[1];
				num_packets+=1
def st_time_map_f2(fn):
	with open(fn) as f:               
		latency_sum = 0
		packet_bytes = 0
		num_packets = 0
		global start_time_map_f2
		for line in f:			
			params= line.split( )	
			if params[0] == '+' and params[2] == '4' and params[3] == '1' and params[4] == 'tcp':				
				start_time_map_f2[params[11]] = params[1];
				num_packets+=1


def calc_latency_f1(file_name):
	with open(file_name) as f: 
		latency_sum = 0
		num_packets = 0
		for line in f:			
			params= line.split( )	
			if params[0] == 'r' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':				
				latency_sum+= float(params[1]) - float(start_time_map_f1[params[11]]) 
				num_packets+= 1
		return str(round(latency_sum/num_packets,3))

def calc_latency_f2(file_name):
	with open(file_name) as f: 
		latency_sum = 0
		num_packets = 0
		for line in f:			
			params= line.split( )	
			if params[0] == 'r' and params[2] == '2' and params[3] == '5' and params[4] == 'tcp':				
				latency_sum+= float(params[1]) - float(start_time_map_f2[params[11]]) 
				num_packets+= 1
		return str(round(latency_sum/num_packets,3))


def filewrite(ln):
	with open('latencyresult.txt','a') as f:
		f.write(ln)
		f.close()	

if os.path.isfile('latencyresult.txt'):
	os.remove('latencyresult.txt')
for x in range(1,11):
	filename='out'
	filename+=str(x)
	line=''
	for y in range(1,5):
		st_time_map_f1(filename+fun(y))
		st_time_map_f2(filename+fun(y))
		line+=calc_latency_f1(filename+fun(y))+'\t'
		line+=calc_latency_f2(filename+fun(y))+'\t'
	filewrite(line+'\n')

		
			
