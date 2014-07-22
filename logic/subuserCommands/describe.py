#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import optparse
#internal imports
import subuserlib.describe,subuserlib.commandLineArguments

def parseCliArgs():
  usage = "usage: subuser %prog [subuser|program] SUBUSER(s)/PROGRAM(s)"
  description = """Show basic information about a subuser or program: Whether it is installed, what it's permissions are ect.
Ex:
$ subuser describe program firefox
<lots of info>
$ subuser describe program firefox
"""
  parser = optparse.OptionParser(usage=usage,description=description,formatter=subuserlib.commandLineArguments.HelpFormatterThatDoesntReformatDescription())
  return parser.parse_args()

(options,args) = parseCliArgs()

for program in args:
  subuserlib.describe.printInfo(program,True)
