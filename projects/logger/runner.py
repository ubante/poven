import logging
import nutslib

"""
DEBUG
INFO
WARNING
ERROR
CRITICAL
"""

logging.basicConfig(filename='slammo.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s %(module)s] %(message)s')
# logging.basicConfig(filename='slammo.log', level=logging.INFO, format='%(asctime)s %(message)s',
#                     datefmt='%m/%d/%Y %I:%M:%S %p')
# logging.basicConfig(format='%(asctime)s %(message)s')
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

logging.critical("")
logging.critical("blank line")
logging.warning('2 this is a warning')
logging.info("this is just info")
logging.debug("this is debugs")

nutslib.methods_outside_classes_are_not_weird()
