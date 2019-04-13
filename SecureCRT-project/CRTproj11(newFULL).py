import os
import subprocess
import csv
#can connect and run in csv only

file = open("commands.txt").read().split("\n")
command_list=list(filter(('').__ne__, file))

file2 = open("ip.txt").read().split("\n")
ip_list=list(filter(('').__ne__, file2))

#select output directory
LOG_DIRECTORY = os.path.join(
	os.path.expanduser('~'), 'LogOutputOfSpecificCommand')

csv_file = open("log.csv","wb+") #dummy file for global variable
worksheet = csv.writer(csv_file) #dummy variable
result_array=[]

SCRIPT_TAB = crt.GetScriptTab()

#--------FUNCTIONS----------------------------------------------------#
def ssh(ip):
	user = "dtacu2000" #username
	passwd = "pwu2k@AAA"
	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1
	SCRIPT_TAB.Screen.Send('\r')
	SCRIPT_TAB.Screen.WaitForString("-bash-3.2$",5)
	SCRIPT_TAB.Screen.Send("ssh -l dtacu2000 "+str(ip) + '\r')
	recon_str="ssh -l dtacu2000 "+str(ip)

	wait_list=["dummy-dummy-dummy","assword:","(yes/no)?","-bash-3.2$","<",">"]
	send_list=["","pwu2k@AAA","yes",recon_str,"",""]

	retry_login = 0 #0=no, 1=yes, 2=fail
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")

	if(nIndex==0):
		temp="LOGIN: ERROR"+" ip: "+ip+ "(can't login)"+"\r"
		worksheet.writerow(['','','',temp])
		return "login_error"
	# else:
	# 	temp="LOGIN: SUCCESS"+" ip: "+ip+ ""+"\r"
	# 	worksheet.writerow(['','','',temp])

	SCRIPT_TAB.Screen.WaitForString("<",1)
	SCRIPT_TAB.Screen.WaitForString(">",1)
	SCRIPT_TAB.Screen.Send("screen-length 0 temporary" + '\r')
	return "login_success"

#---------------------------------------------------
def logout():
	SCRIPT_TAB.Screen.Send("quit" + '\r')
#------------------------------------------------------
def server_login():
	serv_wait_list=["dummy-dummy-dummy","login:","assword:","-bash-3.2$"]
	serv_send_list=["","ossuser","Dtac@6677",""]

	serv_I = SCRIPT_TAB.Screen.WaitForStrings(serv_wait_list,5)
	SCRIPT_TAB.Screen.Send(serv_send_list[(serv_I-1)] + "\n")
	serv_I = SCRIPT_TAB.Screen.WaitForStrings(serv_wait_list,5)
	SCRIPT_TAB.Screen.Send(serv_send_list[(serv_I-1)] + "\n")
	serv_I = SCRIPT_TAB.Screen.WaitForStrings(serv_wait_list,5)
	SCRIPT_TAB.Screen.Send(serv_send_list[(serv_I-1)] + "\n")
	serv_I = SCRIPT_TAB.Screen.WaitForStrings(serv_wait_list,5)
	SCRIPT_TAB.Screen.Send(serv_send_list[(serv_I-1)] + "\n")

	if(serv_I==0):
		temp="SERVER LOGIN ERROR!"
		worksheet.writerow([temp])
		return "serv_error"
	return "serv_success"

#---------------------------------------------------
def LaunchViewer(filename):
	try:
		os.startfile(filename)
	except AttributeError:
		subprocess.call(['open', filename])

#----------------------------------------------------
def NN(number, digitCount):
	# Normalizes a single digit number to have digitCount 0s in front of it
	format = "%0" + str(digitCount) + "d"
	return format % number

#-------RUN FUNCTION-----------------------------------------#

def run_commands(ip_num,COMMANDS):
	# Instruct WaitForString and ReadString to ignore escape sequences when
	# detecting and capturing data received from the remote (this doesn't
	# affect the way the data is displayed to the screen, only how it is handled
	# by the WaitForString, WaitForStrings, and ReadString methods associated
	# with the Screen object.
	SCRIPT_TAB.Screen.IgnoreEscape = True
	SCRIPT_TAB.Screen.Synchronous = True

	# If this script is run as a login script, there will likely be data
	# arriving from the remote system.  This is one way of detecting when it's
	# safe to start sending data. If this script isn't being run as a login
	# script, then the worst it will do is seemingly pause for one second
	# before determining what the prompt is.
	# If you plan on supplying login information by waiting for username and
	# password prompts within this script, do so right before this while loop.
	while True:
		if not SCRIPT_TAB.Screen.WaitForCursor(1):
			break
	# Once the cursor has stopped moving for about a second, we'll
	# assume it's safe to start interacting with the remote system.

	# Get the shell prompt so that we can know what to look for when
	# determining if the command is completed. Won't work if the prompt
	# is dynamic (e.g. changes according to current working folder, etc)
	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1

	prompt = SCRIPT_TAB.Screen.Get(rowIndex, 0, rowIndex, colIndex)
	prompt = prompt.strip()

	global result_array
	result_array=[]
	for (index, command) in enumerate(COMMANDS):
		result="ERROR!!!"
		command = command.strip()

		# Send the command text to the remote
		SCRIPT_TAB.Screen.Send(command + '\r')

		# Wait for the command to be echo'd back to us.
		SCRIPT_TAB.Screen.WaitForString('\r', 1)
		SCRIPT_TAB.Screen.WaitForString('\n', 1)

		# Use the ReadString() method to get the text displayed while
		# the command was runnning.  Note also that the ReadString()
		# method captures escape sequences sent from the remote machine
		# as well as displayed text.  As mentioned earlier in comments
		# above, if you want to suppress escape sequences from being
		# captured, set the Screen.IgnoreEscape property = True.
		result = SCRIPT_TAB.Screen.ReadString(prompt)
		result = result.strip()

		# Write out the results of the command to our log file
		result_array.append(result)
		# result_array.append([ip_num,command])

	# Once we're complete, let's bring up the directory containing the
	# log files.

##----------------calculate Head and Tail-------------------------##
def calHTforTabs(index,numtabs,numlist):
	index=index-1
	cal_size = 0
	cal_head = 0
	cal_tail = 0
	fraction = int(numlist/numtabs)
	remainder = numlist%numtabs
	for i in range(index+1):
		cal_head=cal_tail
		cal_tail=cal_head+fraction
		if(i<remainder):
			cal_tail=cal_tail+1

	return cal_head,cal_tail

##----------------MAIN---------------------------------------##
def main():
	dialog_ans = crt.Dialog.Prompt("What index is this tab: (<tab_index>/<numberOfTabs>)",
                                    "Input Tab index",
                                    "1/1",
                                    False)
	if dialog_ans == "": return csv_file.close()

	tab_index,numberOfTabs = dialog_ans.split("/")
	tab_index = int(tab_index)
	numberOfTabs = int(numberOfTabs)

	# ha=[]
	# ta=[]
	# for i in range(numberOfTabs):
	# 	x,y=calHTforTabs(i+1,numberOfTabs,ip_size)
	# 	ha.append(x)
	# 	ta.append(y)
	# crt.Dialog.MessageBox(str(ha)+"\n"+str(ta))

	global ip_list
	head,tail=calHTforTabs(tab_index,numberOfTabs,ip_size)
	if(head==0 and tail==0):
		return csv_file.close()
	ip_list=ip_list[head:tail]

	#server login
	serv_result = server_login()
	if(serv_result!="serv_success"):
		return csv_file.close()

	if not os.path.exists(LOG_DIRECTORY):
		os.mkdir(LOG_DIRECTORY)

	if not os.path.isdir(LOG_DIRECTORY):
		crt.Dialog.MessageBox(
			"Log output directory %r is not a directory" % LOG_DIRECTORY)
		return csv_file.close()

	if not SCRIPT_TAB.Session.Connected:
		crt.Dialog.MessageBox(
			"Not Connected.  Please connect before running this script.")
		return csv_file.close()

	global csv_file
	global worksheet
	csv_file = open(LOG_DIRECTORY+"/log_"+str(tab_index)+".csv","wb+")
	worksheet = csv.writer(csv_file)
	worksheet.writerow(["IP","COMMANDS","OUTPUTS","ERROR_REPORTS"])

	for ip in ip_list:
		login_result = ssh(ip)
		if(login_result=="login_success"):
			run_commands(ip,command_list)
			maxx=20000
			for i in range(len(command_list)):
				if(len(result_array[i])>=30000):
					loop=(len(result_array[i])//30000)
					if(len(result_array[i])%30000!=0):
						loop=loop+1
					head=0
					tail=0
					for j in range(loop):
						head=tail
						tail=(j+1)*30000
						if(j==0):
							if(i==0):
								worksheet.writerow([ip,command_list[i],result_array[i][head:tail]])
							else:
								worksheet.writerow(["",command_list[i],result_array[i][head:tail]])
						else:
							worksheet.writerow(["","",result_array[i][head:tail]])
				else:
					if(i==0):
						worksheet.writerow([ip,command_list[i],result_array[i]])
					else:
						worksheet.writerow(["",command_list[i],result_array[i]])
		logout()

	SCRIPT_TAB.Screen.Send("echo 'FINISH!''" + '\r')
	csv_file.close()

	if(tab_index==numberOfTabs):
		# crt.Dialog.MessageBox(str(result_array))
		LaunchViewer(LOG_DIRECTORY)


#------------------RUN------------------------------

ip_list=ip_list[:]
ip_size = len(ip_list)
command_list=command_list[:]
# command_list=['ifconfig']
main()

# for i in range(10):
# 	ssh(ip_list[i])
# 	run_commands(ip_list[i],command_list)
# 	logout()
# LaunchViewer(LOG_DIRECTORY)

# ip="10.241.133.178"
# ssh(ip)
# run_commands(ip,command_list)
# logout()
# LaunchViewer(LOG_DIRECTORY)


# run_commands(1,command_list)
#ossuser / Dtac@6677
