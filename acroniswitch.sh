#!/bin/bash

# The script reconnects the Acronis agent to the backup Acronis Management Server if the main one is unavailable. If the primary Acronis Management Server is available and the agent is connected to the backup, then it reconnects to the primary.
# Also, the script monitors the availability of the Acronis Management Server via ICMP and checks if the reconnect command was successful.
#massive - select an array of Acronis Server IP addresses depending on the contour

massive()
{
	#Selecting IP-addresses of the main and backup storages
	local -n IP=$1
	if [[ $(hostname | grep win) ]]
	then	
        	IPIZ=(10.111.15.95 10.111.15.178)
        	IPVN=(10.111.23.101 10.149.25.101)
        	IPIN=(10.111.33.66 10.111.35.162)
	elif [[ $(hostname | grep 02) ]]
	then
		IPIZ=(10.111.15.178 10.111.13.178)
       		IPVN=(10.149.25.101 10.111.23.101)
      		IPIN=(10.111.35.162 10.111.33.66)
	fi
        IP=()
        if [[ $(hostname | grep vn) ]]
        then
                for t in ${IPVN[@]}; do
                        IP+=($t)
                done
        elif [[ $(hostname | grep win) ]]; then
                for t in ${IPIZ[@]}; do
                        IP+=($t)
                done
        else
                for t in ${IPIN[@]}; do
                        IP+=($t)
                done
        fi
}

var=0
massive my_array
for g in ${my_array[@]};
do
	var=$(($var+1))
	#Checking the availability of hypervisor servers with ICMP backup storages
      	cc=$(ping -c4 $g | sed -n '1,/^---/d;s/%.*//;s/.*, //g;p;q')
	if [[ $cc -eq 100 ]]
        then
                if [ $var = 1 ]
                then
			echo $(date +"%Y%m%d-%H%M%S") Backup server $(if [[ $(hostname | grep win) ]]; then echo OCOD; elif [[ $(hostname | grep 02) ]]; then echo RCOD; fi) is not available >> /var/log/acroniswithc.log
			continue
		elif [ $var = 2 ]
		then 
			echo $(date +"%Y%m%d-%H%M%S") Backup server $(if [[ $(hostname | grep win) ]]; then echo RCOD; elif [[ $(hostname | grep 02) ]]; then echo OCOD; fi) is not available >> /var/log/acroniswithc.log
		 	exit
		fi
	else
		if [ $var = 1 ]
                then
                        echo $(date +"%Y%m%d-%H%M%S")  Backup server $(if [[ $(hostname | grep win) ]]; then echo OCOD; elif [[ $(hostname | grep 02) ]]; then echo RCOD; fi) is available >> /var/log/acroniswithc.log
                        #Checking the current Acronis server to which the Acronis agent is connecting
			if [ "$(less /var/lib/Acronis/BackupAndRecovery/MMS/user.config | grep "<address>" | awk '{print $1}' | sed "s/<address>//g" | sed "s%</address>%%g")" = "$g" ]
                        then
                                exit
			else 
				/usr/lib/Acronis/RegisterAgentTool/RegisterAgent -o register -a $g
			fi
			#Switching a Acronis Agent to a Different Acronis Server
                elif [ $var = 2 ]
                then
                        echo $(date +"%Y%m%d-%H%M%S")  Backup server $(if [[ $(hostname | grep win) ]]; then echo RCOD; elif [[ $(hostname | grep 02) ]]; then echo OCOD; fi) is available >> /var/log/kasper.log
			if [ "$(less /var/lib/Acronis/BackupAndRecovery/MMS/user.config | grep "<address>" | awk '{print $1}' | sed "s/<address>//g" | sed "s%</address>%%g")" != "$g" ]
			then
				/usr/lib/Acronis/RegisterAgentTool/RegisterAgent -o register -a $g
			fi
		fi
	fi
done

