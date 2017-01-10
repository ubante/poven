#!/usr/bin/env python

from __future__ import print_function

import argparse
import os
import Queue
import subprocess
import time


def check_if_done(f):
    lines = ['', '']
    max_unreachable_line_len = 100

    # Handle the case when the playbook has just began.
    try:
        f.seek(-max_unreachable_line_len, os.SEEK_END)
    except IOError:
        return False

    for line in f:
        line.rstrip()
        # print(line, end="")
        print(line)
        lines.pop(0)
        lines.append(line)

    print("EOF")

    # print("0:", lines[0])
    # print("1:", lines[1])
    return "unreachable" in lines[0] and lines[1] == "\n"


samplefile = open("sample_file")
if check_if_done(samplefile):
    print("We are done")
else:
    print("not yet done")
