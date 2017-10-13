import os
def fun(x):
    return {
         1: 'tahoe.tr',
         2: 'reno.tr',
	 3: 'newreno.tr',
	 4: 'vegas.tr',
    }.get(x, 'null') 

start_time_map = {};

def st_time_map(fn):
	with open(fn) as f:               
		latency_sum = 0
		packet_bytes = 0
		num_packets = 0
		global start_time_map
		for line in f:			
			params= line.split( )	
			if params[0] == '+' and params[2] == '0' and params[3] == '1' and params[4] == 'tcp':				
				start_time_map[params[11]] = params[1];
				num_packets+=1

def calc_latency(file_name):
	with open(file_name) as f: 
		latency_sum = 0
		num_packets = 0
		for line in f:			
			params= line.split( )	
			if params[0] == 'r' and params[2] == '2' and params[3] == '3' and params[4] == 'tcp':				
				latency_sum+= float(params[1]) - float(start_time_map[params[11]]) 
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
		st_time_map(filename+fun(y))
		line+=calc_latency(filename+fun(y))+'\t'
	filewrite(line+'\n')

		
			
