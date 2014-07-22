#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
#import ...
#internal imports
#import ...

class UserOwnedObject(object):
  __user = None
  def __init__(self,user):
    self.__user = user

  def getUser(self):
    """ Get the User that owns this object. """
    return self.__user
