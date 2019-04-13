import os
import subprocess
import csv
#can connect and run in csv only

## *************** OPEN readme.txt BEFORE USE *************** ##

## Read text from commands.txt and separate between commands and search keywords,
## put them into arrays

file = open("commands.txt").read().split("\n")
command_file=list(filter(('').__ne__, file))
command_list=[]
search_list=[]

for i in range(len(command_file)):
	command_file[i]=command_file[i].split(";key=")
	if(len(command_file[i])>1):
		command_file[i][1]=command_file[i][1].split(",")
		command_list.append(command_file[i][0])
		search_list.append(command_file[i][1])
	else:
		command_list.append(command_file[i][0])
		search_list.append([])

## Read text from ip.txt and put all of ips into an array

file2 = open("ip.txt").read().split("\n")
ip_list=list(filter(('').__ne__, file2))

##	The result will be popped up after running,
##	but the default path would be ..\user\LogOutput
##	You can change the directory name here

LOG_DIRECTORY = os.path.join(
	os.path.expanduser('~'), 'LogOutput')

csv_file = "" #dummy variable for global call
worksheet = "" #dummy variable for glocal call
result_array=[]

SCRIPT_TAB = crt.GetScriptTab()

## ----------------------- FUNCTIONS ----------------------- ##
## To check each ip's connectivity, if the ip is down,
## we will discard that ip and skip to the next one
def ping(ip):
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
## If user wants to change the username and passwd,
## he can change in 'user' and 'passwd' variable
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

	## To avoid errors when running, we put several waiting
	## conditions here.

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

	## After waiting for a long period of time, if no
	## conditions are matched, we will assume that there is
	## some error with the ip, and discard them

	if(nIndex==0):
		temp="LOGIN: ERROR"+" ip: "+ip+ "(can't login)"+"\r"
		worksheet.writerow([ip,'','','',temp])
		return "login_error"
	# else:
	# 	temp="LOGIN: SUCCESS"+" ip: "+ip+ ""+"\r"
	# 	worksheet.writerow(['','','',temp])

	## If we can logged into the ip, the process continues

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

	## The following lines are commands for SecureCRT to be able to detect
	## its screen and read each line from the command's result

	SCRIPT_TAB.Screen.IgnoreEscape = True
	SCRIPT_TAB.Screen.Synchronous = True

	while True:
		if not SCRIPT_TAB.Screen.WaitForCursor(2):
			break

	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1

	global result_array
	result_array=[]

	prompt = SCRIPT_TAB.Screen.Get(rowIndex, 0, rowIndex, colIndex)
	prompt = prompt.strip()

	## This for loop is to read each command in the command_list
	## and send it to SecureCRT, then obtain its output

	for (index, command) in enumerate(COMMANDS):
		result="ERROR!!!" # This is to declare the string variable named 'result'
		command = command.strip()

		SCRIPT_TAB.Screen.Send('\r')
		SCRIPT_TAB.Screen.WaitForString('\r', 10)
		# Send the command text to the remote
		SCRIPT_TAB.Screen.Send(command + '\r')

		# Wait for the command to be echo'd back to us.
		SCRIPT_TAB.Screen.WaitForString('\r', 10)
		SCRIPT_TAB.Screen.WaitForString('\n', 10)

		# Use the ReadString() method to get the text displayed while
		# the command was runnning.
		result = SCRIPT_TAB.Screen.ReadString(prompt)
		result = result.strip()

		# Write out the results of the command to our log file
		result_array.append(result)
	# result_array=list(filter(('').__ne__, result_array))


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

#------------------------------------------------------

## This function will be called when we want to search for
## some certain 'keyword' in the output file.
## The result will be in the separated column from the output,
## The lines will be arranged in the same format as an output,
## but some lines are filtered out.
def searchKey2(result_array,key_list):
	results=[]
	for i in range(len(key_list)):
		if(key_list[i]==[]):
			results.append("") #do nothing, append empty string into the cell
		else:
			result=""
			lines=result_array[i].split("\n")
			for line in lines:
				if any(key in line for key in key_list[i]):
					result=result+line+"\n"
			if(result==""):
				results.append("Not found any result in key="+str(key_list[i]))
			else:
				results.append(str(key_list[i])+" search result:\n"+result)
	return results

## ----------------------- MAIN FUNCTION ----------------------- ##
## This main function will contain all of the functions listed above
def main():
	dialog_ans = crt.Dialog.Prompt("What index is this tab: (<tab_index>/<numberOfTabs>)",
                                    "Input Tab index",
                                    "1/1",
                                    False)

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

	# If the directory does not exist, the script will create it automatically
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
			# Result separation function starts here
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

	## If all the processes are done, the SecureCRT will print out 'FINISH' in the command line
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
ip_size = len(ip_list)

# Indicate the range of commands needed,
# if use all of them, don't change anything here
command_list=command_list[:]

# Let the main program proceeds its function
main()
