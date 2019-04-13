# $language = "python"
# $interface = "1.0"

# Example.py

#########################################################
''' IMPORTS '''

import SecureCRT
import sys
import os
#import time
import datetime as Date
import random

varPath = os.path.dirname(__file__)
if varPath not in sys.path:
    sys.path.insert(0, varPath)
import SecureCRTP
SecureCRTP.Init(crt)


LOG_DIRECTORY = 'C:\\Logs\\'

BANNED_CHARACTERS = ['%', '$', '*', '<', '>', '^', '\'', " ' ", '/', '?', '{', '}', '|', '"', '[', ']']

DATE = str(Date.datetime.now()).split(' ')

# .split(' ')[1].replace(':', '-')[0:8]

try:
    if not os.path.exists(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)
except:
    crt.Dialog.MessageBox('Unable to create C:\Logs\ directory. Please do this manualy now before clicking ok.')
    if not os.path.exists(LOG_DIRECTORY):
        LOG_DIRECTORY = '' # If still not set then set to nothing for local path


def LaunchViewer(filename):
    ''' Opens a file '''
    try:
        os.startfile(filename)
    except AttributeError:
        subprocess.call(['open', filename])

def DCAP(Commands=[], Hostname=None):
    ''' Ready to go data capture function '''
    # If input is only string, convert to tuple
    if type(Commands) == str:
        x = Commands
        Commands = []
        Commands.append(x)

    # If hostname isnt specified then we will
    # use the commands for the filename string
    if Hostname == None:
        try:
            d = str(Date.datetime.now()).split(' ')[0]
            t = str(Date.datetime.now()).split(' ')[1].replace(':', '-')[0:8]
            
            Hostname = 'DCAP_'+str(random.randint(1,10000))+'_Date-'+d+'_Time-'+t
        except:
            Hostname = 'DCAP_'

    Filename = str(Hostname)+'.txt'

    #crt.Dialog.MessageBox(LOG_DIRECTORY+Filename)

    try:
        File = open(LOG_DIRECTORY+Filename, 'wb+')
    except:
        Name = 'DCAP_'+str(random.randint(1,100000000))+'.txt'
        File = open(LOG_DIRECTORY+Name, 'wb+')
    
    for Cmd in Commands:
        strOut = SecureCRTP.Run(str(Cmd))
        File.write('\r\n' * 5)
        File.write('==' * 25)
        File.write('\r\nCommand: '+str(Cmd)+'\r\n')
        File.write('--' * 25)
        File.write('\r\n' * 2)
        File.write(strOut)
        #time.sleep(1)
        
    File.close()

    LaunchViewer(LOG_DIRECTORY)

    return

#########################################################
''' SCRIPT RUNTIME '''

#Hostname = SecureCRTP.Run('sh run | i hostname')
#Hostname = Hostname.replace(' ', '')

#for Character in str(Hostname):
#    if Character in BANNED_CHARACTERS:
#        Character = ''

#crt.Dialog.MessageBox(Hostname)

SecureCRTP.Run('term len 0')

SecureCRTP.Run('conf t')
SecureCRTP.Run('int vlan 10')
SecureCRTP.Run('ip address 192.168.5.55 255.255.255.0')
SecureCRTP.Run('end')
SecureCRTP.Run('wr mem')

Commands = ['show version | i Processor board ID', 'show version | i ROM', \
            'sh version', 'dir', 'show run']
DCAP(Commands)
