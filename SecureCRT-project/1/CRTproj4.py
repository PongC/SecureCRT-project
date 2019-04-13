import os
import subprocess

file = open("commands.txt").read().split("\n")
command_list=list(filter(('').__ne__, file))

file2 = open("ip.txt").read().split("\n")
ip_list=list(filter(('').__ne__, file2))

#select output directory
LOG_DIRECTORY = os.path.join(
	os.path.expanduser('~'), 'LogOutputOfSpecificCommand')

SCRIPT_TAB = crt.GetScriptTab()

#--------FUNCTIONS----------------------------------------------------#
def ssh(ip):
	user = "dtacu2000" #username
	passwd = "pwu2k@AAA" #password
	rowIndex = SCRIPT_TAB.Screen.CurrentRow
	colIndex = SCRIPT_TAB.Screen.CurrentColumn - 1
	check = SCRIPT_TAB.Screen.WaitForString("-bash-3.2$",1)
	SCRIPT_TAB.Screen.Send(str(check)+ '\r')
	# SCRIPT_TAB.Screen.Send("ssh -l dtacu2000 "+str(ip) + '\r')
	# log in condition checking
	conditions=["-bash-3.2$","(yes/no)?","password:","Password:","<"]
	send=["yes","pwu2k@AAA","pwu2k@AAA","none","none"]
	error_count=0
	while_break=0
	while(True):
		for i in range(len(conditions)):
			check = SCRIPT_TAB.Screen.WaitForString(conditions[i],3)
			SCRIPT_TAB.Screen.Send(conditions[i]+str(check)+ '\r')
			if(conditions[i]=="<" and check==1):
				check = SCRIPT_TAB.Screen.WaitForString(">",1)
				if(check==1):
					while_break=1
					break
			elif(check==1):
				SCRIPT_TAB.Screen.Send(send[i] + '\r')

		# no condition matched
		error_count=error_count+1
		if(error_count>=3):
			# if no condition matched twice
			SCRIPT_TAB.Screen.Send("echo 'LOGIN: ERROR (no condition matched)'" + '\r')
			while_break=1
		if(while_break==1):
			break

	SCRIPT_TAB.Screen.Send("screen-length 0 temporary" + '\r')

#---------------------------------------------------
def logout():
	SCRIPT_TAB.Screen.Send("quit" + '\r')

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

	if not os.path.exists(LOG_DIRECTORY):
		os.mkdir(LOG_DIRECTORY)

	if not os.path.isdir(LOG_DIRECTORY):
		crt.Dialog.MessageBox(
			"Log output directory %r is not a directory" % LOG_DIRECTORY)
		return

	if not SCRIPT_TAB.Session.Connected:
		crt.Dialog.MessageBox(
			"Not Connected.  Please connect before running this script.")
		return

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


	for (index, command) in enumerate(COMMANDS):
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

		FOLDER_DIRECTORY=LOG_DIRECTORY+"\output"+str(ip_num)
		if not os.path.exists(FOLDER_DIRECTORY):
		    os.makedirs(FOLDER_DIRECTORY)

		filep = open(FOLDER_DIRECTORY+"/Command_"+str(index)+"_result.txt","wb+")

		# folder_name = "\output"+str(index_num)
		# direct = os.path.join(LOG_DIRECTORY,folder_name)
		# filep = open(direct+"/Command_"+str(index)+"_Results.txt", 'wb+')

		# If you don't want the command logged along with the results, comment
		# out the very next line
		filep.write("Results of command: " + command + os.linesep)

		# Write out the results of the command to our log file
		filep.write(result + os.linesep)

		# Close the log file
		filep.close()

	# Once we're complete, let's bring up the directory containing the
	# log files.

##----------------MAIN---------------------------------------##



# for ip in ip_list:
# 	ssh(ip)
# 	run_commands(ip,command_list)
# 	logout()
# LaunchViewer(LOG_DIRECTORY)

# for i in range(10):
# 	ssh(ip_list[i])
# 	run_commands(ip_list[i],command_list)
# 	logout()
# LaunchViewer(LOG_DIRECTORY)

ip="10.241.133.178"
ssh(ip)
# run_commands(ip,command_list)
# logout()
# LaunchViewer(LOG_DIRECTORY)


# run_commands(1,command_list)
#ossuser / Dtac@6677
