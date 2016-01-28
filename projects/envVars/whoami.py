#!/usr/bin/env python


import os
import pwd

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

print "You are ", get_username()





