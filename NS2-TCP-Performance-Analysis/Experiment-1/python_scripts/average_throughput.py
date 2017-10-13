from __future__ import division
import os
with open('tpresult.txt','r') as f:
	thr_sum_tahoe = 0
	thr_sum_reno = 0
	thr_sum_newreno = 0
	thr_vegas = 0
	for line in f:
		params=line.split( )
		thr_sum_tahoe+=float(params[0]) 
		thr_sum_reno+=float(params[1])
		thr_sum_newreno+=float(params[2])
		thr_vegas+= float(params[3]) 
	print (thr_sum_tahoe/10)
	print (thr_sum_reno/10)
	print (thr_sum_newreno/10)
	print (thr_vegas/10)        
