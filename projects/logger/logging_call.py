import logging
import sys
from subprocess import (call, check_output, CalledProcessError)

"""
Intercept call output to STDOUT and log instead.

thanks: http://stackoverflow.com/questions/3979888/in-python-scipting-how-do-i-capture-output-from-subprocess-call-to-a-file
"""

command = ["ls", "-la"]

# this line shows what happens when call returns an error
# command = ["ls", "-la", "doesnotexistfile"]

print "Straight to the terminal:"
call(command)

print "To logging:"
logging.basicConfig(filename="os.log", level=logging.DEBUG)
logging.debug("")
logging.debug("Start")

try:
    # output = check_output(['ls', '-a', '-l'])
    output = check_output(command)
except CalledProcessError as e:
    return_code = e.returncode
    logging.critical("command failed: {}".format(return_code))
else:
    ctr = 0
    for line in output.split("\n"):
        ctr += 1
        logging.debug(str(ctr) + " " + line)
sys.stdout.flush()

logging.debug("Finished")
logging.debug("")
print "Finished"


