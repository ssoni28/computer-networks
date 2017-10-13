i=1
while [ $i -lt 11 ]
do
   ns tahoe.tcl $i
   i=`expr $i + 1`
done
i=1
while [ $i -lt 11 ]
do
   ns newreno.tcl $i
   i=`expr $i + 1`
done
i=1
while [ $i -lt 11 ]
do
   ns reno.tcl $i
   i=`expr $i + 1`
done
i=1
while [ $i -lt 11 ]
do
   ns vegas.tcl $i
   i=`expr $i + 1`
done
 

