import logging
import sys
from subprocess import (call, check_output, CalledProcessError, Popen, PIPE)

"""
Intercept call output to STDOUT and log instead.

thanks: http://stackoverflow.com/questions/3979888/in-python-scipting-how-do-i-capture-output-from-subprocess-call-to-a-file
"""

command = ["ls", "-la"] # the good line
# command = ["ls", "-la", "doesnotexistfile"] # the bad line

print "Straight to the terminal:"
sys.stdout.flush()
call(command)

print "To logging:"
logging.basicConfig(filename="os.log", level=logging.DEBUG)
logging.debug("")
logging.debug("Start")

output = Popen(command, stdout=PIPE, stderr=PIPE)
stdout, stderr = output.communicate()

if stdout:
    ctr = 0
    for line in stdout.split("\n"):
        ctr += 1
        logging.debug("[" + str(ctr) + "]: " + line)

if stderr:
    ctr = 0
    for line in stderr.split("\n"):
        ctr += 1
        logging.error("[" + str(ctr) + "]: " + line)


logging.debug("Finished")
logging.debug("")
print "Finished"


