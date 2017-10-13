
#Define a 'finish' procedure
proc finish {} {
	global tf
        close $tf
        exit 0
}

#Create a simulator object
set ns [new Simulator]
set tf [open [format "out%dnrv.tr" $argv] w]
$ns trace-all $tf
#Create four nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]


#Create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail


#Setup a TCP connection
set tcp [new Agent/TCP/Newreno]
$tcp set class_ 1
$ns attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Setup a TCP connection
set tcp2 [new Agent/TCP/Vegas]
$tcp2 set class_ 2
$ns attach-agent $n5 $tcp2
set sink2 [new Agent/TCPSink]
$ns attach-agent $n6 $sink2
$ns connect $tcp2 $sink2
$tcp2 set fid_ 2

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP
$ftp set filesize_ 0x1000

#Setup a FTP over TCP connection
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
$ftp2 set type_ FTP
$ftp2 set filesize_ 0x1000

#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n2 $udp
set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp $null
$udp set fid_ 3

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set random_ false
$cbr set rate_ [format "%dmb" $argv]

#Schedule events for the CBR and FTP agents
$ns at 0.1 "$cbr start"
$ns at 1.0 "$ftp start"
$ns at 1.0 "$ftp2 start"
$ns at 10.0 "$ftp2 stop"
$ns at 10.0 "$ftp stop"
$ns at 10.5 "$cbr stop"

#Call the finish procedure after 5 seconds of simulation time
$ns at 11.0 "finish"


#trace file


    

    #Run the simulation
             
$ns run 






