from __future__ import division
import os
with open('latencyresult.txt','r') as f:
	lat_sum_tahoe = 0
	lat_sum_reno = 0
	lat_sum_newreno = 0
	lat_vegas = 0
	for line in f:
		params=line.split( )
		lat_sum_tahoe+=float(params[0]) 
		lat_sum_reno+=float(params[1])
		lat_sum_newreno+=float(params[2])
		lat_vegas+= float(params[3]) 
	print (lat_sum_tahoe/10)
	print (lat_sum_reno/10)
	print (lat_sum_newreno/10)
	print (lat_vegas/10)        
