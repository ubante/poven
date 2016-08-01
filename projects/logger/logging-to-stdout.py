import logging
import sys

# from http://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log
# see https://docs.python.org/3/library/logging.html#logrecord-attributes for details

logging.basicConfig(filename='slammo.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s %(module)s] %(message)s')

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelno)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

logging.critical("both? - crit")
logging.error("both? - error")
logging.warning("both? - warn")
logging.info("both? - info")
logging.debug("both? - debug")
print

ch.setLevel(logging.INFO)
logging.critical("both? - crit")
logging.error("both? - error")
logging.warning("both? - warn")
logging.info("both? - info")
logging.debug("both? - debug")
print

print "Lettuce play a game."

