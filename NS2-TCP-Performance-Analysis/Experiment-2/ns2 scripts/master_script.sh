i=1
while [ $i -lt 11 ]
do
   ns rr.tcl $i
   i=`expr $i + 1`
done
i=1
while [ $i -lt 11 ]
do
   ns nrr.tcl $i
   i=`expr $i + 1`
done
i=1
while [ $i -lt 11 ]
do
   ns vv.tcl $i
   i=`expr $i + 1`
done
i=1
while [ $i -lt 11 ]
do
   ns nrv.tcl $i
   i=`expr $i + 1`
done
 

