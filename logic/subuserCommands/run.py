#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

import sys

import subuserlib.run,subuserlib.update

##############################################################
def printHelp():
  print("""Run a program installed with subuser.  For example:
$ subuser run firefox

This command is useful if you want to put `~/subuser/bin` at the end of your path.  If you do that, subuser programs will not have precidence over "normally" installed programs.
""")

def getArgsToPassToProgram():
  if len(sys.argv) > 2:
    return sys.argv[2:]
  else:
    return []

#################################################################################################
if len(sys.argv) == 1 or sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
  printHelp()
  sys.exit()
#################################################################################################

programName = sys.argv[1]
subuserlib.run.runProgram(programName,getArgsToPassToProgram())
