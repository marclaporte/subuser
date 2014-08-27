#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import sys,os,optparse
#internal imports
import subuserlib.availablePrograms,subuserlib.install,subuserlib.describe,subuserlib.commandLineArguments

def parseCliArgs():
  usage = "usage: subuser %prog [options] PROGRAM_NAME(s)"
  description = """Install a set of subuser programs.  To view a list of programs that can be installed try:

$ subuser list available
"""
  parser=optparse.OptionParser(usage=usage,description=description,formatter=subuserlib.commandLineArguments.HelpFormatterThatDoesntReformatDescription())
  advancedOptions = subuserlib.commandLineArguments.advancedInstallOptionsGroup(parser)
  parser.add_option_group(advancedOptions)
  return parser.parse_args()

#################################################################################################

options,userProgramList = parseCliArgs()

for program in userProgramList:
  print(program)
  subuserlib.install.installProgramAndDependencies(program, options.useCache)

print("\n============= INSTALLATION SUCCESSFULL =============\n\n")
for program in userProgramList:
  print("\n"+program+": has been installed with the following permissions.")
  subuserlib.describe.printInfo(program,False)
  print("You can change this program's permissions at any time by editing it's permissions.json file.")
