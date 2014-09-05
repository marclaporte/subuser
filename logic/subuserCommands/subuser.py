#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import sys,optparse
#internal imports
import subuserlib.classes.user,subuserlib.resolve,subuserlib.classes.subuser,subuserlib.verify, subuserlib.commandLineArguments,subuserlib.update

def parseCliArgs():
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
  return parser.parse_args()

#################################################################################################

options,args = parseCliArgs()

action = args[0]

user = subuserlib.classes.user.User()

if action == "add":
  if not len(args) == 3:
    sys.exit("Wrong number of arguments to add.  See `subuser subuser -h`.")
  name = args[1]
  imageSourceId = args[2]
#  try:
  if True:
    imageSource = subuserlib.resolve.resolveImageSource(user,imageSourceId)
    user.getRegistry().logChange("Adding subuser "+name+" "+imageSourceId)
    user.getRegistry().getSubusers()[name] = subuserlib.classes.subuser.Subuser(user,name,imageSource,None,False)
    subuserlib.verify.verify(user)
    user.getRegistry().commit()
    """
  except Exception as e:
    print("Adding subuser failed.")
    print(str(e))
    subuserlib.update.checkoutNoCommit(user,"HEAD")
"""
    
elif action == "remove":
  name = args[1]
  if name in user.getRegistry().getSubusers():
    user.getRegistry().logChange("Removing subuser "+name)
    del user.getRegistry().getSubusers()[name]
    subuserlib.verify.verify(user)
    user.getRegistry().commit()
  else:
    sys.exit("Cannot remove: subuser "+name+" does not exist.")
elif action == "create-shortcut":
  name = args[1]
  user.getRegistry().logChange("Creating shortcut for subuser "+name)
  user.getRegistry().getSubusers()[name].setExecutableShortcutInstalled(True) 
  subuserlib.verify.verify(user)
  user.getRegistry().commit()
elif action == "remove-shortcut":
  name = args[1]
  user.getRegistry().logChange("Removing shortcut for subuser "+name)
  user.getRegistry().getSubusers()[name].setExecutableShortcutInstalled(False)
  subuserlib.verify.verify(user)
  user.getRegistry().commit()
  
