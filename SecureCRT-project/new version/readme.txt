============================= README =============================

Edited on 04 AUG 2017 09:14

USER MANUAL for the SecureCRT's python script and .exe file

0. AVAILABLE FILES
	- commands.txt
	- ip.txt
	- runningSimulator.exe (for pseudo-parallel purpose)
	- CRTproj.py (actual script that can be run manually also)
	- readme.txt

1. REQUIREMENTS
	1.1 Two text files, namely "commands.txt" and "ip.txt"
	1.2 BOTH of the text files have to be in the
		SAME folder as the PYTHON script
	1.3 RECOMMENDATION: put 2 text files, .py script, and the .exe file
		in the SAME folder

2. EXPECTED RESULTS
	2.1 After the script finishes, the program should launch a folder
		named "LogOutput" which is located in "..\user\" directory
	2.2 There will be 1 (or more) log file(s) according to the number of
		TABS used in running the script
		EX. if we have 100 ips and 10 tabs running the script concurrently,
			there will be 10 log files in the folder
		NOTE: The log file is in .csv format but accessible by Excel
	2.3 In each log file, there will be certain columns listed as
		IP | COMMAND | OUTPUT | SEARCH_RESULT | ERROR_REPORT
		NOTE: in output cells, there maybe several cells for an output
		because of the limitation in cell's capacity, so 1 output maybe
		divided in several parts (cells), but can be copied and pasted normally

3. FOR COMMANDS.TXT
	There are 2 options available for obtaining log files,
	so there are 2 formats for each line in commands.txt as follow
	3.1 ONLY OUTPUT: = normal command line
		EX. display version, display interface, etc.
		NOTE: all of the commands can be written in its short form
	3.2 OUTPUT + KEY_SEARCH: = normal command line + ';key=' + 'KEYWORD'
		There will be a normal output in OUTPUT column; however,
		if user wants to filter some 'KEYWORDS' the result will be
		in the 'SEARCH_RESULT' column in the log file, for example
			dis ver;key=version information:,PBG
		the result of 'dis ver' command will be in OUTPUT column, while
		the result of lines with keywords 'version information:' or 'PBG'
		will be in the 'SEARCH_RESULT' column and the rest will be discarded
		**you can put as many keywords as you want, but each keywords must be
		separated with ","
	FORMAT:
		[<COMMAND>]
			or
		[<COMMAND>;key=<key1>,<key2>,<key3>,...]
	EX
		dis ver;key=version information,PBG,Software
		dis isis peer;key=total peer
		dis inter

4. FOR IP.TXT
	4.1 list all of the ips that will be used in the text file
		NOTE: Users don't have to worry about wrong ip number or such,
		the script will handle the error and report it in log file

5. HOW TO USE THE PROGRAM
	5.1 Open SecureCRT program
	5.2 ** Run the script ONCE before using the runningSimulator **
		This is to make the program notice the script's location.
		In addition, the script will prompt a dialog at first and we can
		cancel it, so we don't actually RUN the whole program here.
	5.3 Open 'runningSimulator.exe'
	5.4 Type number of TABS to run the script
		NOTE: To avoid errors and such, a suggestion would be 1 to 4 tabs.
		      Compatible number of tabs may vary due to the computer specification.
		      In fact, the program is capable to run up to 10 tabs at a time,
		      but the error will occur more frequent due to overload computer resources usage.
		      So, we suggest user to find the most compatible number of tabs by your own
		      user experience. (Try from 10 and reduce the number until you not found any errors)
	5.5 Switch back to SecureCRT and let the simulator processes
		** WARNING: DON'T switch to other programs until the simulation is finished. **
		Make sure that you have other important tasks done beforehand.
	5.6 When finish, the script will launch a directory automatically
		The result will be shown in .csv file that separated up to your selected number of tabs
	
