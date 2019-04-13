import os
import subprocess

SCRIPT_TAB = crt.GetScriptTab()
SCRIPT_TAB.Screen.Send("echo 'yes'" + '\r')


    # result= SCRIPT_TAB.Screen.WaitForString('yes',1)
    # if(result==1):
    #     SCRIPT_TAB.Screen.Send("echo 'true'"+str(result) + '\r')
    # else:
    #     SCRIPT_TAB.Screen.Send("echo 'false'"+str(result)+ '\r')

while(1):
    result= SCRIPT_TAB.Screen.WaitForString('yes')
    SCRIPT_TAB.Screen.Send(str(result)+"\r")

#1=found, 0=timeout
# error_count=0
# while(True):
# 	if(SCRIPT_TAB.Screen.WaitForString("(yes/no)?",1)==1):
# 		SCRIPT_TAB.Screen.Send("yes" + '\r')
# 	elif(SCRIPT_TAB.Screen.WaitForString("Password:",1)==1):
# 		SCRIPT_TAB.Screen.Send("pwu2k@AAA" + '\r')
# 	elif(SCRIPT_TAB.Screen.WaitForString("password:",1)==1)
# 		SCRIPT_TAB.Screen.Send("pwu2k@AAA" + '\r')
# 	elif(SCRIPT_TAB.Screen.WaitForString("<",1)==1):
# 		if(SCRIPT_TAB.Screen.WaitForString(">",1)==1):
# 			break
# 	else:
# 		error_count=error_count+1
# 		if(error_count==2):
#             SCRIPT_TAB.Screen.Send("echo 'LOGIN: ERROR (no condition matched)'" + '\r')
# 			break

# SCRIPT_TAB.Screen.Send("ssh -l dtacu2000 10.241.133.178"+ '\r')
# SCRIPT_TAB.Screen.WaitForString("password:",3)
# SCRIPT_TAB.Screen.Send("echo 'yoyoyo lolona'"+"\r")
# # SCRIPT_TAB.Screen.WaitForString("password:",3)
# SCRIPT_TAB.Screen.Send("echo lololo2"+"\r")
