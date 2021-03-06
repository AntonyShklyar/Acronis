#!/usr/bin/python

'''
Tested on Python versions 2.7.13 and 3.5.3

The script reconnects the Acronis agent to the backup Acronis Management Server if the main one is unavailable. If the primary Acronis Management Server is available and the agent is connected to the backup, then it reconnects to the primary.
Also, the script monitors the availability of the Acronis Management Server via ICMP and checks if the reconnect command was successful.
'''

import os
import socket
import subprocess
import re

def logs():
        '''Creating a session log and a log with a description of all sessions'''
        #If the size of 1 GB is exceeded, the acronis.log is deleted and recreated
        if not os.path.exists('/var/log/acronis.log'): 
            f = open('/var/log/acronis.log', "w+")
            f.close()
        if not os.path.getsize('/var/log/acronis.log')/(1024*1024*1024) == 0:
            os.system(r' >/var/log/acronis.log')
	'''
        Output data:
        the function returns 0
        '''
def networkavailable(var, g):
	'''Determining the network availability of Acronis Management Server'''
        mount = subprocess.Popen(("ping", "-c4", g), stdout=subprocess.PIPE)
        exit_code = subprocess.check_output(("sed", "-n", '1,/^---/d;s/%.*//;s/.*, //g;p;q'), stdin=mount.stdout).decode("utf-8")
        if int(exit_code.replace("\n","")) == 100:
            if var == 1:
                os.system('echo $(date +"%Y%m%d-%H%M%S")     Acronis Server is not available       >> /var/log/acronis.log')
                return 1
            else:
                os.system('echo $(date +"%Y%m%d-%H%M%S")     Acronis Server is not available       >> /var/log/acronis.log')
                return 1
        else:
                os.system('echo $(date +"%Y%m%d-%H%M%S")   Acronis Server is available      >> /var/log/acronis.log')
                return 0
	'''
	Input data:
        var - data type is a number - Counter
        g - data type is a string - IP-address of Acronis Management Server
        Output data:
        Return data type - number.
        If the function returns 0 - Acronis Management Server is available
        If the function returns 1 - Acronis Management Server isn't available
	'''
'''
Editable parameters:
--segment
The data type is a dictionary.
Data - domain: list of IP addresses Acronis server and segments
--codid
The data type is a dictionary.
Data - Data Center ID: IP Acronis server
'''
segment = {'ac.com': ['10.111.15.56', '10.111.15.65', '10.111.15.77'], 'vp.com': ['10.111.16.56', '10.111.16.65', '10.111.16.77'], 'in.com': ['10.111.17.56', '10.111.17.65', '10.111.17.77']}
codid = {'01': ['10.111.15.56', '10.111.16.56', '10.111.17.56'], '02': ['10.111.15.65', '10.111.16.65', '10.111.17.77'], '03': ['10.111.15.77', '10.111.16.77', '10.111.17.77']}
#Determining the massive, which will be filled IP-addresses Acronis Management Server
acronis = []
logs()
#Determining the server name
a = socket.gethostname()
for x, y in segment.items():
    if x in a:
        for z in y:
            acronis.append(y)
for x, y in codid.items():
    for z in y:
        if x in a and z in acronis:
            acronis.remove(z)
            acronis.insert(0, z)
for var, g in enumerate(acronis, 1):
        b = networkavailable(var, g)
        if b == 0:
            cmd = "less /var/lib/Acronis/BackupAndRecovery/MMS/user.config | grep '<address>' | awk '{print $1}'" 
            pipe = os.popen(cmd)
            a = pipe.read()
            a=a.replace("\n","")
            a = re.sub('<address>','',a)
            a = re.sub('/<address>','',a)
            if a == g and (var == 1 or var != 1):
                os.system('echo $(date +"%Y%m%d-%H%M%S") Agent Acronis connected to server '+g+' >> /var/log/acronis.log')
                exit()
            elif var == 1:
                if subprocess.call(["/usr/lib/Acronis/RegisterAgentTool/RegisterAgent", "-o", "register", "-a", g]) == 0: 
                    os.system('echo $(date +"%Y%m%d-%H%M%S") Server Acronis change operation '+g+' Successful >> /var/log/acronis.log')
                    exit()
                else:
                    os.system('echo $(date +"%Y%m%d-%H%M%S") Server Acronis change operation on '+g+' Unsuccessful >> /var/log/acronis.log')
                    exit()
            elif a != g and var != 1:
                if subprocess.call(["/usr/lib/Acronis/RegisterAgentTool/RegisterAgent", "-o", "register", "-a", g]) == 0: 
                    os.system('echo $(date +"%Y%m%d-%H%M%S") Server Acronis change operation '+g+' Successful >> /var/log/acronis.log')
                    exit()
                else:
                    os.system('echo $(date +"%Y%m%d-%H%M%S") Server Acronis change operation on '+g+' Unsuccessful >> /var/log/acronis.log')
                    exit()
        elif var != len(acronis):
            continue
        else:
            os.system('echo $(date +"%Y%m%d-%H%M%S") Servers Acronis '+str(acronis)+' unavailable >> /var/log/acronis.log')
            exit()
