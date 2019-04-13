import os
import subprocess
import csv
#can connect and run in csv only

## both of the text file must be in the same folder as the script ##

file = open("commands.txt").read().split("\n")
command_file=list(filter(('').__ne__, file))
command_list=[]
search_list=[]
#read text from commands.txt and separate between commands and search keywords
for i in range(len(command_file)):
	command_file[i]=command_file[i].split(";key=")
	if(len(command_file[i])>1):
		command_file[i][1]=command_file[i][1].split(",")
		command_list.append(command_file[i][0])
		search_list.append(command_file[i][1])
	else:
		command_list.append(command_file[i][0])
		search_list.append([])

# crt.Dialog.MessageBox(str(command_file)+"\n\n"+str(command_list)+"\n\n"+str(search_list))


file2 = open("ip.txt").read().split("\n")
ip_list=list(filter(('').__ne__, file2))

##	The result will be popped up after running,
##	but the default path would be ..\user\LogOutputOfSpecificCommand

LOG_DIRECTORY = os.path.join(
	os.path.expanduser('~'), 'LogOutput')

csv_file = "" #dummy variable for global call
worksheet = "" #dummy variable for glocal call
result_array=[]

SCRIPT_TAB = crt.GetScriptTab()

## ----------------------- FUNCTIONS ----------------------- ##
def ping(ip):
	#to check whether the ip is alive or not
	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1
	wait_list=["dummy-dummy-dummy","alive","no answer"]
	send_list=["","",""]

	SCRIPT_TAB.Screen.Send('\r')
	SCRIPT_TAB.Screen.WaitForString("-bash-3.2$",5)
	SCRIPT_TAB.Screen.Send('ping '+ip+' 10\r')
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list)
	if(nIndex==2):
		return "alive"
	else:
		return "no answer"

## Login to each IP via this function
def ssh(ip):
	user = "dtacu2000" # each IP's username
	passwd = "pwu2k@AAA" # each IP's password
	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1
	SCRIPT_TAB.Screen.Send('\r')
	SCRIPT_TAB.Screen.WaitForString("-bash-3.2$",5)
	SCRIPT_TAB.Screen.Send("ssh -l "+user+" "+str(ip) + '\r')
	recon_str="ssh -l "+user+" "+str(ip)

	#********you can edit ssh conditions here***********
	wait_list=["assword:","(yes/no)?","-bash-3.2$","<",">"]
	send_list=[passwd,"yes",recon_str,"",""]

	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list,8)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list,5)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list,5)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list,5)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list,8)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list,5)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list,5)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")
	nIndex = 0
	nIndex = SCRIPT_TAB.Screen.WaitForStrings(wait_list,5)
	SCRIPT_TAB.Screen.Send(send_list[(nIndex-1)] + "\n")

	if(nIndex==0):
		temp="LOGIN: ERROR"+" ip: "+ip+ "(can't login)"+"\r"
		worksheet.writerow([ip,'','','',temp])
		return "login_error"
	# else:
	# 	temp="LOGIN: SUCCESS"+" ip: "+ip+ ""+"\r"
	# 	worksheet.writerow(['','','',temp])

	SCRIPT_TAB.Screen.WaitForString("<",3)
	SCRIPT_TAB.Screen.WaitForString(">",1)
	SCRIPT_TAB.Screen.Send("screen-length 0 temporary" + '\r')
	SCRIPT_TAB.Screen.WaitForString(">",5)
	return "login_success"

#------------------------------------------------------
def logout():
	SCRIPT_TAB.Screen.Send("quit" + '\r')
#------------------------------------------------------

## Login to the server via this function
def server_login():
	#****edit server login conditions here
	serv_wait_list=["login:","assword:","-bash-3.2$"]
	# The username and password of the server can be edited here
	serv_send_list=["ossuser","Dtac@6677",""]

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

#------------------------------------------------------
def LaunchViewer(filename):
	try:
		os.startfile(filename)
	except AttributeError:
		subprocess.call(['open', filename])

#------------------------------------------------------
def NN(number, digitCount):
	# Normalizes a single digit number to have digitCount 0s in front of it
	format = "%0" + str(digitCount) + "d"
	return format % number

#------------------------------------------------------

## This function is used to run commands in each IP according to the list

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
		if not SCRIPT_TAB.Screen.WaitForCursor(2):
			break
	# Once the cursor has stopped moving for about a second, we'll
	# assume it's safe to start interacting with the remote system.

	# Get the shell prompt so that we can know what to look for when
	# determining if the command is completed. Won't work if the prompt
	# is dynamic (e.g. changes according to current working folder, etc)
	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1

	global result_array
	result_array=[]

	prompt = SCRIPT_TAB.Screen.Get(rowIndex, 0, rowIndex, colIndex)
	prompt = prompt.strip()

	for (index, command) in enumerate(COMMANDS):
		result="ERROR!!!"
		command = command.strip()

		SCRIPT_TAB.Screen.Send('\r')
		SCRIPT_TAB.Screen.WaitForString('\r', 5)
		# Send the command text to the remote
		SCRIPT_TAB.Screen.Send(command + '\r')

		# Wait for the command to be echo'd back to us.
		SCRIPT_TAB.Screen.WaitForString('\r', 5)
		SCRIPT_TAB.Screen.WaitForString('\n', 5)
		# SCRIPT_TAB.Screen.WaitForString('\n', 1)

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
		# result_array.append(command)
		# result_array.append([ip_num,command])

	# Once we're complete, let's bring up the directory containing the
	# log files.

#------------------------------------------------------

## This function is used to calculate IP numbers for each tab
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

#----------------------------------------------------------#

def searchKey(result_array,key_list):
	#separate each key and output separately, doesn't keep the format of the output
	results=[]
	for i in range(len(key_list)):
		if(key_list[i]==[]):
			results.append("") #do nothing
		else:
			result=""
			lines=result_array[i].split("\n")
			for key in key_list[i]:
				result=result+"Keyword: "+key+"\n"
				for line in lines:
					if(key in line):
						result=result+"   "+line+"\n"
				result=result+"-------------\n"
			results.append(result)
	return results

def searchKey2(result_array,key_list):
	#keep the format of the output and print out only lines that contain some of the keys
	results=[]
	for i in range(len(key_list)):
		if(key_list[i]==[]):
			results.append("") #do nothing
		else:
			result=""
			lines=result_array[i].split("\n")
			for line in lines:
				if any(key in line for key in key_list[i]):
					result=result+line+"\n"
			results.append(result)
	return results



## ----------------------- MAIN FUNCTION ----------------------- ##
def main():
	dialog_ans = crt.Dialog.Prompt("What index is this tab: (<tab_index>/<numberOfTabs>)",
                                    "Input Tab index",
                                    "1/1",
                                    False)
	# if dialog_ans == "": return csv_file.close()
	if dialog_ans == "": return ""

	# Number of tabs is indicated in the other python script,
	# but this program will fetch the number and calculate the
	# IPs needed for each tab respectively

	tab_index,numberOfTabs = dialog_ans.split("/")
	tab_index = int(tab_index)
	numberOfTabs = int(numberOfTabs)

	global ip_list
	head,tail=calHTforTabs(tab_index,numberOfTabs,ip_size)
	if(head==0 and tail==0):
		return csv_file.close()
	ip_list=ip_list[head:tail]

	# Log-in to the server first, if not success the procedure won't resume
	serv_result = server_login()
	if(serv_result!="serv_success"):
		return csv_file.close()

	#if the directory is not exist, create one
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

	# Create an output file and indicate its format
	# CSV file could be accessed normally by Microsoft Excel

	csv_file = open(LOG_DIRECTORY+"/log_"+str(tab_index)+".csv","wb+")
	worksheet = csv.writer(csv_file)
	worksheet.writerow(["IP","COMMANDS","OUTPUTS","SEARCH_RESULTS","ERROR_REPORTS"])

	# This loop is just to write an result out from each command
	# to its corresponding IP, but
	# each cell in Excel has the limit of 32767 characters,
	# so we will have to split the exceed output into several cells

	for ip in ip_list: # for each ip
		ping_result = ping(ip)
		if(ping_result=="alive"):
			login_result = ssh(ip) # ssh first
		else:
			login_result = "login_failed"
			worksheet.writerow([ip,"","","","ERROR: "+ip+" is not alive!"])

		if(login_result=="login_success"):
		# if it can be acessed normally, then retrieve its output
			run_commands(ip,command_list)
			sresults=searchKey2(result_array,search_list)
			################################-----------------------------------------------------function HERE------------------------##
			maxx=20000 # limit each cell's maximum character at 20,000
			for i in range(len(command_list)):
				if(len(result_array[i])>=30000):
					#if the result exceed 30000 characters, cut it in to n blocks
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
								worksheet.writerow([ip,command_list[i],result_array[i][head:tail],sresults[i][head:tail]])
							else:
								worksheet.writerow(["",command_list[i],result_array[i][head:tail],sresults[i][head:tail]])
						else:
							worksheet.writerow(["","",result_array[i][head:tail]])
				else:
					if(i==0):
						worksheet.writerow([ip,command_list[i],result_array[i],sresults[i]])
					else:
						worksheet.writerow(["",command_list[i],result_array[i],sresults[i]])
		logout()

	SCRIPT_TAB.Screen.Send('\r')
	SCRIPT_TAB.Screen.WaitForString("-bash-3.2$",5)
	SCRIPT_TAB.Screen.Send("echo 'FINISH!'" + '\r')
	csv_file.close()

	if(tab_index==numberOfTabs):
		# crt.Dialog.MessageBox(str(result_array))
		# The output will be resulted as soon as the script's finished
		LaunchViewer(LOG_DIRECTORY)


## ------------- DECLARE VARIABLES and RUN THE MAIN PROGRAM HERE ------------- ##

# Indicate the range of IPs needed,
# if use all of them, don't change anything here
ip_list=ip_list[:]
# ip_list=ip_list+["192.111.111.111"]
# ip_list=ip_list+ip_list

ip_size = len(ip_list)

# Indicate the range of commands needed,
# if use all of them, don't change anything here
command_list=command_list[:]

# command_list=['ifconfig']

# Let the main program proceeds its function
main()







#-----------test---------

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
