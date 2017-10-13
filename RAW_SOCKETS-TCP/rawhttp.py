''''
    Raw sockets on Linux
    FCN Project4
'''
                           # Import Stataments
#==============================================================================
# imports statements
import fcntl
import struct
import collections
import random
import socket, sys
import os
import os.path
from struct import *                        
#==============================================================================

#==============================================================================  
                           # Global Variables
#==============================================================================
output_file=''
relative_path = '/'
remote_host=''
source_ip =''
dest_ip =''
tcp_source = random.randint(5000,6000)   # source port
tcp_dest = 80   # destination port
d = {}
connection_timeout = 0
#==============================================================================  
                           # URL Parse Function
#==============================================================================
# url_parse: URL
# This function parse the url being provided at the command line

def url_parse(url):
	global output_file
	global relative_path
	global remote_host
	ua=url.split('/')
	remote_host = ua[2]
	LastIndex = len(ua) - 1
	path='/'
	if (LastIndex > 2):
		if (ua[LastIndex].find('.') and ua[LastIndex] != ''):
			output_file = ua[LastIndex]
			relative_path += "/".join(ua[3:LastIndex+1])
		else:
			output_file = 'index.html'		
			relative_path += "/".join(ua[3:LastIndex+1])
	else:
		output_file = 'index.html'	
#==============================================================================


#==============================================================================  
                           # Source IP Fucntion
#==============================================================================
    
def get_interface_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("www.ccs.neu.edu", 80))
	source_ipaddr = s.getsockname()[0]
	
	return source_ipaddr
	
#==============================================================================
#==============================================================================  
                           # checksum function
#==============================================================================
# checksum(msg) : Header -> Checksum
# This function calculates checksum of given TCP or IP header

def checksum(msg):
    s = 0
    if len(msg) % 2 == 1:
		msg += "\0" 
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
		w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
		s = s + w
		s = (s & 0xffff) + ( s>>16 ) 
    #complement and mask to 4 byte short
    s = ~s & 0xffff 
    return s
#==============================================================================


#==============================================================================
                             # IP Validations
#==============================================================================
# ipheader_validation(Protocol,Header,Checksum) -> Boolean
# This function verifies whether the IP checksum and protocol id of received 
# packet is valid or not

def ipheader_validation(incoming_protocol,ip_header,ip_check):
 	# Calculate checksum	
	check = checksum(ip_header)
	# change to big endian format
	ip_check = struct.pack('>H', ip_check)
	ip_check = struct.unpack('H', ip_check)[0]
        if (check == ip_check and incoming_protocol == socket.IPPROTO_TCP):
		return True
    	else:
		return False
#==============================================================================

		
#==============================================================================
                             # TCP Validations
#==============================================================================
# tcpheader_validation(Checksum,Header,Source_IP,Destination_IP,Header_Length,
# Data_Length,Data) -> Boolean
# This function verifies whether the TCP checksum of received packet is valid
# or not

def tcpheader_validation(incoming_checksum,header,source,dest,header_length,data_length,data):
	# pseudo header fields	
	placeholder = 0
	protocol = 6
	tcp_length =  header_length + data_length
	pseudo_header = pack('!4s4sBBH' , source, dest, placeholder, protocol ,tcp_length);
	# tcp header for checksum calculation
	final_header = pseudo_header + header
	# calculate checksum
	check = checksum(final_header)
	# change to big endian format
	incoming_checksum = struct.pack('>H', incoming_checksum)
	incoming_checksum = struct.unpack('H', incoming_checksum)[0]
	if (incoming_checksum == check):
		return True 
	else:	
		return False	
	
#==============================================================================
                             # Create IP Header
#==============================================================================
# ipheader(Source_IP, Destination_IP) -> IP Header
# This function creates IP Header by taking source IP address and destination 
# IP address

def ipheader(source_ip,dest_ip):
	# ip header fields
	ip_ihl = 5
	ip_ver = 4
	ip_tos = 0
	ip_tot_len = 0  # kernel will fill the correct total length
	ip_id = 54321   #Id of this packet
	ip_frag_off = 0
	ip_ttl = 255
	ip_proto = socket.IPPROTO_TCP
	ip_check = 0    # kernel will fill the correct checksum
	ip_saddr = socket.inet_aton ( source_ip )   
	ip_daddr = socket.inet_aton ( dest_ip )
	ip_ihl_ver = (ip_ver << 4) + ip_ihl
	# the ! in the pack format string means network order
	ip_header = pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
	return ip_header
#==============================================================================


#==============================================================================
                             # Create TCP Header
#==============================================================================
# tcpheader(Sequence_no, Ack_Seq_no, Fin, Syn, Ack, Data) -> TCP Header
# This function creates a TCP Header by taking randomly generated sequence no

def tcpheader(tcp_psh,tcp_seq,tcp_ack_seq,tcp_fin,tcp_syn,tcp_ack,userdata):
	
	# tcp header fields
	tcp_doff = 5    #4 bit field, size of tcp header, 5 * 4 = 20 bytes

	#tcp flags
	tcp_rst = 0
	
	tcp_urg = 0
	tcp_window = socket.htons (5840)    #   maximum allowed window size
	tcp_check = 0
	tcp_urg_ptr = 0
	tcp_offset_res = (tcp_doff << 4) + 0
	tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp_urg << 5)
	# the ! in the pack format string means network order
	tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window, tcp_check, tcp_urg_ptr)
	# pseudo header fields	
	source_address = socket.inet_aton( source_ip )
	dest_address = socket.inet_aton(dest_ip)
	placeholder = 0
	protocol = socket.IPPROTO_TCP
	tcp_length = len(tcp_header) + len(userdata)
	
	# pack pseudo header
	psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
	# create header to calculate checksum
	psh = psh + tcp_header + userdata;
	# calculate checksum 
	tcp_check = checksum(psh)
	 
	# make the tcp header again and fill the correct checksum - checksum 
        # is NOT in network byte order
	tcp_header = pack('!HHLLBBH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,  tcp_window) + pack('H' , tcp_check) + pack('!H' , tcp_urg_ptr)
	return tcp_header

#==============================================================================


#==============================================================================
                             # Filter Incoming packets
#==============================================================================
# this function filters incoming packets intended for this application
def filter_incoming_packets(incoming_pkt_addr,prot,incoming_pkt_dest_port):
	return ((incoming_pkt_addr == dest_ip) and (prot == socket.IPPROTO_TCP)
and (incoming_pkt_dest_port == tcp_source))
    
#==============================================================================


#==============================================================================
                             # Handshake
#==============================================================================
# handshake(): 
# This function initiates the SYN request and sends it to destination in order 
# to create connection with it.
# After SYN,ACK is recieved from the destination, we sends ACK to the 
# destination and that is how three way handshake gets accomplished.
init_seq_num = 0
pktsfiltered = 0
bytes_claimed = 0
def handshake():
	global init_seq_num
	global d
	global connection_timeout
	global pktsfiltered
	global bytes_claimed
	packet = '';	 	
	ip_header=ipheader(source_ip,dest_ip)
	tcp_seq = random.randint(1,65535)
	tcp_ack_seq = 0
	tcp_fin = 0
	tcp_syn = 1
	tcp_ack = 0
	tcp_psh=0
	userdata=''
	tcp_header=tcpheader(tcp_psh,tcp_seq,tcp_ack_seq,tcp_fin,tcp_syn,tcp_ack,userdata)
	 
	# final full packet - syn packets dont have any data
	packet = ip_header + tcp_header
	 
	#Send the packet finally - the port specified has no effect
	s.sendto(packet, (dest_ip , 0 ))    

	data = '';
	flag = True
	ConnectionActive = True
	ConnectionTearDown = False
	initial = True
	sndpacket = ''
	isIpValidated = True
	isTcpValidated = True
	total_data_received = 0
	sndpacket_prev = sndpacket
	while ConnectionActive:	
		try:
			packet = r.recvfrom(65535)
     
			#packet string from tuple
			packet = packet[0]
			connection_timeout = 0
			# IP Header
			#take first 20 characters for the IP header
			ip_header = packet[0:20]
			# Set the checksum field to 0 in IP header	
			ip_header_val = list(ip_header)
			ip_header_val[10] ='\0'
			ip_header_val[11] = '\0'
			ip_new_header ="".join(ip_header_val)
			#now unpack the IP header
			iph = unpack('!BBHHHBBH4s4s' , ip_header)			
			# IP Header fields after unpacking
			version_ihl = iph[0]
			version = version_ihl >> 4         # IP Version
			ihl = version_ihl & 0xF    
			iph_length = ihl * 4            # Header Length	
			ip_total_length = iph[2]

			ttl = iph[5]                       # Time To Live
			protocol = iph[6]                  # Protocol
			i_check = iph[7]	           # checksum
			s_addr = socket.inet_ntoa(iph[8]); # Source IP
			d_addr = socket.inet_ntoa(iph[9]); # Destination IP
			
			# Check IP validations on incoming packet
			isChksumValidated = ipheader_validation(protocol,ip_new_header,i_check)
			
# TCP Header         
			tcp_header = packet[iph_length:(iph_length+20)]
			#now unpack the TCP header
			tcph = unpack('!HHLLBBHHH' , tcp_header)
			# TCP Header fields after unpacking
			source_port = tcph[0]               # Source Port
			dest_port = tcph[1]	            # Destination Port
			sequence = tcph[2] 		    # Sequence No
			acknowledgement = tcph[3]  	    # Acknowledgement No
			doff_reserved = tcph[4]      	    # Data Offset
			flags = tcph[5]			    # TCP flags
			t_check = tcph[7]		    # Checksum
			
			if (filter_incoming_packets(s_addr,protocol,dest_port)):
				if (initial):				
					init_seq_num = sequence			
				syn_flag_status = flags & 0x02
				fin_flag_status = flags & 0x01
				ack_flag_status = flags & 0x10
				rst_flag_status = flags & 0x04
				tcph_length = doff_reserved >> 4
				h_size = iph_length + tcph_length * 4
				
				data_size = len(packet) - h_size
				data = packet[h_size:]
				server_bytes = sequence- init_seq_num
				server_bytes -= 1
				bytes_claimed += len(data)

				# Set checksum field to 0 in TCP header
				tcp_header = packet[iph_length:]
				tcp_header_validation = list(tcp_header)
				tcp_header_validation[16] ='\0'
				
				
				tcp_header_validation[17] ='\0'
				tcp_new_header = "".join(tcp_header_validation)
				# Check validation of TCP Checksum of incoming packet
				isTcpValidated = tcpheader_validation(t_check,tcp_new_header,iph[8],iph[9],tcph_length * 4,data_size,data)
				 
				packet = '';	 		
				ip_header_snd=ipheader(source_ip,dest_ip)
				tcp_seq = acknowledgement
				if (ConnectionTearDown == True):
					ConnectionActive = False
				if ((syn_flag_status ==  0x02) or (fin_flag_status ==  0x01) or ((ack_flag_status == 0x10) and (data_size == 0))):
					tcp_ack_seq = sequence + 1 
				else:
					tcp_ack_seq = sequence + len(data)
					total_data_received += len(data)
					pktsfiltered += 1

				if (fin_flag_status ==  0x01 or rst_flag_status == 0x04):
					ConnectionTearDown = True
					tcp_fin = 1
				else:
					tcp_fin = 0	
				
					
				if (ConnectionActive):
					tcp_syn = 0
					tcp_ack = 1
					userdata = ''
					tcp_psh = 0
					tcp_header_snd=tcpheader(tcp_psh,tcp_seq,tcp_ack_seq,tcp_fin,tcp_syn,tcp_ack,userdata)	 
					# final full packet - syn packets dont have any data
					sndpacket = ip_header_snd + tcp_header_snd
					if (syn_flag_status == 0x02):
						s.sendto(sndpacket, (dest_ip , 0 ))
					if (not ((ack_flag_status == 0x10) and (data_size == 0) and (ConnectionTearDown == False))):
						if (isChksumValidated and ( len(data) ==  (bytes_claimed - server_bytes))):   # If validations falied, don't send ACK
							d[sequence]=data
							sndpacket_prev = sndpacket
							s.sendto(sndpacket, (dest_ip , 0 ))
						else:
							if (len(data) !=  (bytes_claimed - server_bytes)):
								bytes_claimed -= len(data)
							s.sendto(sndpacket_prev, (dest_ip , 0 )) 
							continue
						
					if (flag): 
						if (isChksumValidated):
							initial = False 
							packet = '';	 
							ip_header=ipheader(source_ip,dest_ip)
							tcp_seq = acknowledgement
							tcp_ack_seq = int(sequence) + 1 
							tcp_fin = 0
							tcp_syn = 0
							tcp_ack = 1
							tcp_psh = 1
							userdata = "GET "+relative_path+" HTTP/1.1\r\n" + "Host: "+remote_host+"\r\n" + "Connection: keep-alive\r\n"+"\r\n"
							tcp_header=tcpheader(tcp_psh,tcp_seq,tcp_ack_seq,tcp_fin,tcp_syn,tcp_ack,userdata)	 
							# final full packet - syn packets dont have any data
							sndpacket = ip_header + tcp_header + userdata
							s.sendto(sndpacket, (dest_ip , 0 )) 
							r.settimeout(60)
							flag = False
						else:
			 				print 'Incoming TCP Header = '+ str(tcp_header).encode("hex") + 'Data_size ='+str(hex(data_size))+ ' Incoming IP header = ' + str(ip_header).encode("hex") 
							continue
		except socket.timeout:
			print "Retransmit in case of no ACK"
			if ( connection_timeout == 3 ):
				print 'Server Not Responding: Closing Connection'
				ConnectionActive = False
			else:
				connection_timeout += 1
				s.sendto(sndpacket_prev, (dest_ip , 0 )) 
#==============================================================================
	
#==============================================================================
                             # Create Raw Sockets
#==============================================================================
	
if (len(sys.argv) == 2):
	url = sys.argv[1]
	url_parse(url)
else:
	print 'Incorrect arguments. Please run as "./rawhttpget <URL>"'
	sys.exit()
	
source_ip = get_interface_ip()
dest_ip=socket.gethostbyname(remote_host)
#Create sender and receiver raw sockets
try:
    # Sender Socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
    # Reciever Socket
    r = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    r.settimeout(180) 
    #r.connect((remote_host, 80))
    r.settimeout(60)
except socket.error , msg:
    print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
if (os.path.isfile(output_file)):
	os.remove(output_file)    
handshake()
s.close()
r.close()

od = collections.OrderedDict(sorted(d.items()))
with open(output_file, "a") as myfile:
	for key, value in od.items():
		myfile.write(value)
lines = ''		

with open(output_file, "r") as myfile1:	
	lines=myfile1.readlines()
writetoopfile=False
ith open(output_file, "w") as myfile2:
	for line in lines:
		if(writetoopfile):
			myfile2.write(line)
		if(line == "\r\n"):
			writetoopfile=True

#==============================================================================
                             # End Of File
#==============================================================================



