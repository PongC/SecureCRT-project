# $language = "python"
# $interface = "1.0"

# This script demonstrates how Python scripting can be used to interact
# with CRT and manipulate an spreadsheet file (for reading by other
# programs such as Microsoft Excel). This script uses Python's csv library
# to create a spreadsheet, then it sends a command to a remote server
# (assuming we're already connected). It reads the output, parses it and
# writes out some of the data to the spreadsheet and saves it.  This
# script also demonstrates how the WaitForStrings function can be used to
# wait for more than one output string.
#
import os
import csv

def main():

	crt.Screen.Synchronous = True

	# Create an Excel compatible spreadsheet
	#
	filename = 'chart.csv'
	fileobj = open(filename, 'wb')

	worksheet = csv.writer(fileobj)

	# Send the initial command to run and wait for the first linefeed
        # Command to print its result
	crt.Screen.Send("ifconfig"+"\r")
	crt.Screen.WaitForString("\n")

	# Create an array of strings to wait for.
	#
	promptStr = "[student@test1 ~]$"
	waitStrs = [ "\n", promptStr ]

	row = 1

	output = ''

	while True:

		# Wait for the linefeed at the end of each line, or the shell
		# prompt that indicates we're done.
		#
		result = crt.Screen.WaitForStrings( waitStrs )

		#result = index number + 1

		# We saw the prompt, we're done.
		#
		if result == 2:
			break

		# Fetch current row and read the first 40 characters from the
		# screen on that row. Note, since we read a linefeed character
		# subtract 1 from the return value of CurrentRow to read the
		# actual line.
		#
		screenrow = crt.Screen.CurrentRow - 1
		readline = crt.Screen.Get(screenrow, 1, screenrow, 40)
		
                readline = readline.strip()

		# Split the line ( ":" delimited) and put some fields into Excel
		#

		output = output+readline+"\n"
		
		row = row + 1

        worksheet.writerow([output])
        
                
	fileobj.close()
	crt.Screen.Synchronous = False


main()
