#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import sys,optparse
#internal imports
import subuserlib.classes.user,subuserlib.commandLineArguments,subuserlib.subuser

def parseCliArgs(sysargs):
  usage = "usage: subuser %prog [add|remove|create-shortcut] NAME IMAGESOURCE"
  description = """

Add and remove subusers.  Create shorcuts for launching subusers.

$ subuser subuser add foo foo@default

$ subuser subuser remove foo

$ subuser subuser create-shorcut foo

$ subuser subuser remove-shortcut foo
"""
  parser=optparse.OptionParser(usage=usage,description=description,formatter=subuserlib.commandLineArguments.HelpFormatterThatDoesntReformatDescription())
  advancedOptions = subuserlib.commandLineArguments.advancedInstallOptionsGroup(parser)
  parser.add_option_group(advancedOptions)
  return parser.parse_args(args=sysargs[1:])

def subuser(user,sysargs):
  """
  >>> import subuser #import self
  >>> import subuserlib.classes.user
  >>> user = subuserlib.classes.user.User()
  >>> user.getRegistry().getSubusers().keys()
  [u'foo']
  >>> subuser.subuser(user,["subuser","add","bar","bar@file:///home/travis/remote-test-repo"])
  Adding subuser bar bar@file:///home/travis/remote-test-repo
  Verifying subuser configuration.
  Verifying registry consistency...
  Unregistering any non-existant installed images.
  Checking if images need to be updated or installed...
  Installing bar ...
  Installed new image for subuser bar
  Running garbage collector on temporary repositories...
  >>> user.getRegistry().getSubusers().keys()
  [u'foo', 'bar']
  >>> subuser.subuser(user,["subuser","remove","bar"])
  Removing subuser bar
  Verifying subuser configuration.
  Verifying registry consistency...
  Unregistering any non-existant installed images.
  Checking if images need to be updated or installed...
  Running garbage collector on temporary repositories...
  >>> user.getRegistry().getSubusers().keys()
  [u'foo']
  """
  options,args = parseCliArgs(sysargs)
  action = args[0]
  if action == "add":
    if not len(args) == 3:
      sys.exit("Wrong number of arguments to add.  See `subuser subuser -h`.")
    name = args[1]
    imageSourceId = args[2]
    subuserlib.subuser.add(user,name,imageSourceId)
  elif action == "remove":
    name = args[1]
    subuserlib.subuser.remove(user,name)
  elif action == "create-shortcut":
    name = args[1]
    subuserlib.subuser.setExecutableShortcutInstalled(user,name,True)
  elif action == "remove-shortcut":
    name = args[1]
    subuserlib.subuser.setExecutableShortcutInstalled(user,name,False)
  else:
    sys.exit("Action "+args[0]+" does not exist. Try:\n subuser subuser --help")
#################################################################################################




  
if __name__ == "__main__":
  user = subuserlib.classes.user.User()
  subuser(user,sys.argv)