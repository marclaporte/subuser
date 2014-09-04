#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
#import ...
#internal imports
import subuserlib.classes.userOwnedObject,subuserlib.dockerImages,subuserlib.dockerPs

class InstalledImage(subuserlib.classes.userOwnedObject.UserOwnedObject):
  __imageID = None
  __lastUpdateTime = None
  __programSourceName = None
  __sourceRepoId = None

  def __init__(self,user,imageID,programSourceName,sourceRepoId,lastUpdateTime):
    subuserlib.classes.userOwnedObject.UserOwnedObject.__init__(self,user)
    self.__imageID = imageID
    self.__lastUpdateTime = lastUpdateTime
    self.__programSourceName = programSourceName
    self.__sourceRepoId = sourceRepoId

  def getImageID(self):
    return self.__imageID

  def getSourceRepoId(self):
    return self.__sourceRepoId

  def getProgramSourceName(self):
    return self.__programSourceName

  def getLastUpdateTime(self):
    return self.__lastUpdateTime

  def isDockerImageThere(self):
    """
     Does the Docker daemon have an image with this imageID?
    """
    return not subuserlib.dockerImages.inspectImage(self.getImageId()) == None

  def removeDockerImage(self):
    """
      Remove the image from the Docker daemon's image store.
    """
    subuserlib.dockerImages.removeImage(self.getImageID())
