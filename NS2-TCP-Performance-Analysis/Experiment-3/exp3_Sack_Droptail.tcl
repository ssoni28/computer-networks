#Create a simulator object
set ns [new Simulator]


#trace file
set tf [open sack_droptail_out.tr w]


#Create six nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]


#Define a 'finish' procedure
proc finish {} {
        global tf
        close $tf
        exit 0
}

$ns trace-all $tf  

#Define different colors for dats flows
$ns color 1 red ;# the color of packets from n1
$ns color 5 blue ;# the color of packets from n5

#Create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n3 $n6 10Mb 10ms DropTail

#Setup a TCP connection
set tcp [new Agent/TCP/Sack1]
$tcp set class_ 2
$ns attach-agent $n1 $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set null [new Agent/UDP]
$ns attach-agent $n6 $null
$ns connect $udp $null
$udp set fid_ 2

#Setup a CBR over UDP connection
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ 10mb
$cbr set random_ false

#Schedule events for the CBR and FTP agents
$ns at 0.1 "$ftp start"
$ns at 3.0 "$cbr start"
$ns at 10.0 "$ftp stop"
$ns at 10.0 "$cbr stop"

$ns at 10.0 "finish"



$ns run



