#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import sys
#internal imports
import subuserlib.classes.user,subuserlib.resolve,subuserlib.classes.subuser,subuserlib.verify,subuserlib.update

def add(user,subuserName,imageSourceIdentifier):
  try:
    try:
      imageSource = subuserlib.resolve.resolveImageSource(user,imageSourceIdentifier)
    except KeyError as keyError:
      sys.exit("Could not add subuser.  The image source "+imageSourceIdentifier+" does not exist.")
    user.getRegistry().logChange("Adding subuser "+subuserName+" "+imageSourceIdentifier)
    user.getRegistry().getSubusers()[subuserName] = subuserlib.classes.subuser.Subuser(user,subuserName,imageSource,None,False)
    subuserlib.verify.verify(user)
    user.getRegistry().commit()
  except subuserlib.classes.dockerDaemon.ImageBuildException as e:
    print("Adding subuser failed.")
    print(str(e))
    subuserlib.update.checkoutNoCommit(user,"HEAD")

def remove(user,subuserName):
  if subuserName in user.getRegistry().getSubusers():
    user.getRegistry().logChange("Removing subuser "+subuserName)
    del user.getRegistry().getSubusers()[subuserName]
    subuserlib.verify.verify(user)
    user.getRegistry().commit()
  else:
    sys.exit("Cannot remove: subuser "+subuserName+" does not exist.")

def setExecutableShortcutInstalled(user,subuserName,installed):
  if installed:
    user.getRegistry().logChange("Creating shortcut for subuser "+subuserName)
  else:
    user.getRegistry().logChange("Removing shortcut for subuser "+subuserName)
  user.getRegistry().getSubusers()[subuserName].setExecutableShortcutInstalled(installed)
  subuserlib.verify.verify(user)
  user.getRegistry().commit()