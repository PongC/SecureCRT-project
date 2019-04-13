# $language = "python"
# $interface = "1.0"

# Connect to an SSH server using the SSH2 protocol. Specify the
# username and password and hostname on the command line as well as
# some SSH2 protocol specific options.
import multiprocessing.dummy import Pool

host = "10.241.133.178" #host IP
host2 = "10.241.133.183"
h = [host, host2]


def login(host):
	# Prompt for a password instead of embedding it in a script...
	#
	# passwd = crt.Dialog.Prompt("Enter password for " + host, "Login", "", True)
	user = "dtacu2000" #username
	passwd = "pwu2k@AAA"

	# Build a command-line string to pass to the Connect method.
	cmd = "/SSH2 /L %s /PASSWORD %s /C 3DES /M MD5 %s" % (user, passwd, host)
	crt.Session.Connect(cmd)


login(host)
login(host2)

pool = Pool(4)
pool.map(login,h)
