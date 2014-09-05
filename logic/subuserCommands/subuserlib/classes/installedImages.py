#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import os,json,collections,sys
#internal imports
import subuserlib.classes.installedImage,subuserlib.classes.fileBackedObject, subuserlib.classes.userOwnedObject

class InstalledImages(dict,subuserlib.classes.userOwnedObject.UserOwnedObject,subuserlib.classes.fileBackedObject.FileBackedObject):

  def reloadInstalledImagesList(self):
    """ Reload the installed images list from disk, discarding the current in-memory version. """
    self.clear()

    installedImagesPath = self.getUser().getConfig().getInstalledImagesDotJsonPath()
    if os.path.exists(installedImagesPath):
      with open(installedImagesPath, 'r') as file_f:
        try:
          installedImagesDict = json.load(file_f, object_pairs_hook=collections.OrderedDict)
        except ValueError:
          sys.exit("Error:  installed-images.json is not a valid JSON file. Perhaps it is corrupted.")
    else:
      installedImagesDict = {}
    # Create the InstalledImage objects.
    for imageId,imageAttributes in installedImagesDict.iteritems():
      image = subuserlib.classes.installedImage.InstalledImage(
        user=self.getUser(),
        imageId=imageId,
        imageSourceName=imageAttributes["image-source"],
        sourceRepoId=imageAttributes["source-repo"], 
        lastUpdateTime=imageAttributes["last-update-time"])
      self[imageId]=image
 
  def save(self):
    """ Save attributes of the installed images to disk. """
    # Build a dictionary of installed images.
    installedImagesDict = {}
    for _,installedImage in self.iteritems():
      imageAttributes = {}
      imageAttributes["last-update-time"] = installedImage.getLastUpdateTime()
      imageAttributes["image-source"] = installedImage.getImageSourceName()
      imageAttributes["source-repo"] = installedImage.getSourceRepoId()
      installedImagesDict[installedImage.getImageId()] = imageAttributes

    # Write that dictionary to disk.
    installedImagesPath = self.getUser().getConfig().getInstalledImagesDotJsonPath()
    with open(installedImagesPath, 'w') as file_f:
      json.dump(installedImagesDict, file_f, indent=1, separators=(',', ': '))

  def __init__(self,user):
    subuserlib.classes.userOwnedObject.UserOwnedObject.__init__(self,user)
    self.reloadInstalledImagesList()

  def unregisterNonExistantImages(self):
    """
     Go through the installed images list and unregister any images that aren't actually installed.
    """
    for imageId,image in self.iteritems():
      if not image.isDockerImageThere():
        del self[imageId]
