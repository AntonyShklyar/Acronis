#!/usr/bin/python

import os
import socket
import subprocess
import re

#Events are written to the log file /var/log/backup.log. When the log size reaches 1 GB, it is deleted and recreated.
if not os.path.exists('/var/log/backupdb.log'): open("/var/log/backupdb.log", "w+")
#If the size of 1 GB is exceeded, the debug.log is deleted and recreated
if not os.path.getsize('/var/log/backupdb.log')/(1024*1024*1024)==0: os.remove('/var/log/backupdb.log')

def massive(IP=[]):
	if set('01').issubset(socket.gethostname()):
        	IPIZ = ["10.111.15.95", "10.111.15.57"]
                IPVN = ['10.111.23.102', '10.149.25.102']
                IPIN = ['10.111.33.67', '10.111.35.163']
        elif set('02').issubset(socket.gethostname()):
        	IPIZ = ['10.111.16.195', '10.111.15.137']
                IPVN = ['10.149.25.102', '10.111.23.102']
                IPIN = ['10.111.35.163', '10.111.33.67']	
	if socket.gethostname().find('vn.com') >= 0:
		for i in IPVN:
			IP.append(i)
	elif socket.gethostname().find('iz.com') >= 0:
                for i in IPIZ:
                        IP.append(i)
	else:
		for i in IPIN:
                        IP.append(i)
	return IP
def networkavailable(var, g):
        mount = subprocess.Popen(("ping", "-c4", g), stdout=subprocess.PIPE); exit_code = subprocess.check_output(("sed", "-n", '1,/^---/d;s/%.*//;s/.*, //g;p;q'), stdin=mount.stdout); mount.wait()
        if int(exit_code.replace("\n","")) == 100:
                if var==1:
                        os.system('echo $(date +"%Y%m%d-%H%M%S")     Acronis Server is not available       >> /var/log/backupdb.log')
                        return 1
                else:
                        os.system('echo $(date +"%Y%m%d-%H%M%S")     Acronis Server is not available       >> /var/log/backupdb.log')
                        return 1
        else:
                os.system('echo $(date +"%Y%m%d-%H%M%S")   Acronis Server is available      >> /var/log/backupdb.log')
                return 0
var=0
my_array=massive()
for g in my_array:
        var += 1
        b=networkavailable(var, g)
        if b==0:
                cmd = "less /var/lib/Acronis/BackupAndRecovery/MMS/user.config | grep '<address>' | awk '{print $1}'" 
		pipe = os.popen(cmd)
		a = pipe.read()
		a=a.replace("\n","")
		a = re.sub('<address>','',a)
		a = re.sub('/<address>','',a)
		if a==g and var==1:
                        exit()
		elif var==1:
			if subprocess.call(["/usr/lib/Acronis/RegisterAgentTool/RegisterAgent", "-o", "register", "-a", g]) == 0: os.system('echo $(date +"%Y%m%d-%H%M%S") Acronis Server change operation Successful >> /var/log/backupdb.log'); exit()
			else:
				os.system('echo $(date +"%Y%m%d-%H%M%S") Acronis Server change operation Unsuccessful >> /var/log/backupdb.log'); exit()
		elif a!=g and var==2:
			if subprocess.call(["/usr/lib/Acronis/RegisterAgentTool/RegisterAgent", "-o", "register", "-a", g]) == 0: os.system('echo $(date +"%Y%m%d-%H%M%S") Acronis Server change operation Successful >> /var/log/backupdb.log'); exit()
	elif var != len(my_array):
		continue
        else:
                exit()
