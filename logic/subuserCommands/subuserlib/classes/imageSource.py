#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import subprocess,os
#internal imports
import subuserlib.classes.userOwnedObject,subuserlib.classes.describable,subuserlib.subprocessExtras,subuserlib.resolve

class ImageSource(subuserlib.classes.userOwnedObject.UserOwnedObject,subuserlib.classes.describable.Describable):
  __name = None
  __repo = None
  __permissions = None

  def __init__(self,user,repo,name):
    subuserlib.classes.userOwnedObject.UserOwnedObject.__init__(self,user)
    self.__name = name
    self.__repo = repo

  def getName(self):
    return self.__name

  def getRepository(self):
    return self.__repo

  def getSubusers(self):
    """
     Get a list of subusers that were built from this ImageSource.
    """
    subusers = []
    for subuser in self.getUser().getRegistry().getSubusers():
      if subuser.getImageSource()==self:
        subusers.append(subuser)
    return subusers

  def getSourceDir(self):
    return os.path.join(self.getRepository().getRepoPath(),self.getName())

  def getBuildType(self):
    """
     Return the build type for this image source.  Or None, if no valid build files are found.  Possible build types are:
       - 'SubuserImagefile'
       - 'BuildImage.sh'
    """
    dockerImageDir = os.path.join(self.getSourceDir(),"docker-image")
    pathToBuildTypeMap = {
      "SubuserImagefile" : os.path.join(dockerImageDir,"SubuserImagefile"),
      "BuildImage.sh" : os.path.join(dockerImageDir,"BuildImage.sh")}
    buildType = None
    for type,path in pathToBuildTypeMap.iteritems():
      if os.path.isfile(path):
        buildType = type
    return buildType 

  def getLatestInstalledImage(self):
    """
    Get the most up-to-date InstalledImage based on this ImageSource.
    Returns None if no images have been installed from this ImageSource.
    """
    lastUpdateTime=''
    mostUpToDateImage = None
    for installedImage in self.getInstalledImages():
      if installedImage.getLastUpdateTime() > lastUpdateTime:
        mostUpToDateImage = installedImage
    return mostUpToDateImage

  def getInstalledImages(self):
    """
    Return the installed images which are based on this image.
    """
    installedImagesBasedOnThisImageSource = []
    for _,installedImage in self.getUser().getInstalledImages().iteritems():
      if installedImage.getImageSourceName() == self.getName() and installedImage.getSourceRepoId() == self.getRepository().getName():
        installedImagesBasedOnThisImageSource.append(installedImage)
    return installedImagesBasedOnThisImageSource

  def getPermissions(self):
    if not self.__permissions:
      permissionsPath=os.path.join(self.getSourceDir(),"permissions.json")
      self.__permissions = subuserlib.classes.permissions.Permissions(self.getUser(),readPath=permissionsPath,writePath=permissionsPath)
    return self.__permissions

  def describe(self):
    print(self.getName()+":")
    self.getPermissions().describe()

  def getSubuserImagefileContents(self):
    """
     Returns the contents of the SubuserImagefile.  If there is no SubuserImagefile, raises an exception.
    """
    dockerImageDir = os.path.join(self.getSourceDir(),"docker-image")
    subuserImageFilePath = os.path.join(dockerImageDir,"SubuserImagefile")
    if os.path.isfile(subuserImageFilePath):
      with open(subuserImageFilePath,mode="r") as subuserImageFile:
        return subuserImageFile.read()
    else:
      raise Exception("This ImageSource does not build from a SubuserImagefile.")

  def generateDockerfileConents(self,parent=None):
    """
    Returns a string representing the Dockerfile that is to be used to build this ImageSource.
    """
    subuserImagefileContents = self.getSubuserImagefileContents()
    dockerfileContents = ""
    for line in subuserImagefileContents.split("\n"):
      if line.startswith("FROM-SUBUSER-IMAGE"):
        dockerfileContents = dockerfileContents + "FROM "+parent+"\n"
      else:
        dockerfileContents = dockerfileContents +line+"\n"
    return dockerfileContents

  def getDependency(self):
    """
     Returns the dependency of this ImageSource as a ImageSource.
     Or None if there is no dependency.
    """
    SubuserImagefileContents = self.getSubuserImagefileContents()
    lineNumber=0
    for line in SubuserImagefileContents.split("\n"):
      if line.startswith("FROM-SUBUSER-IMAGE"):
        try:
          return subuserlib.resolve.resolveImageSource(self.getUser(),line.split(" ")[1],contextRepository=self.getRepository(),allowRefferingToRepositoriesByName=False) #TODO, ImageSource names with spaces or other funny characters...
        except IndexError:
          raise Exception("Syntax error in SubuserImagefile one line"+str(lineNumber)+":\n"+line)
      lineNumber+=1
    return None
  
