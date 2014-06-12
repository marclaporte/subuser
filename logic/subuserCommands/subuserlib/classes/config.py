#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import os,inspect,json
#internal imports
import subuserlib.classes.userOwnedObject,subuserlib.loadMultiFallbackJsonConfigFile

class Config(subuserlib.classes.userOwnedObject.UserOwnedObject):
  __config = None

  def _getSubuserConfigPaths(self):
    """ Returns a list of paths to config.json files in order that they should be looked in. """
    configFileInHomeDir = os.path.join(self.getUser().homeDir,".subuser","config.json")
    configFileInEtc = "/etc/subuser/config.json"
    configFileInSubuserDir = os.path.join(getSubuserDir(),"config.json")
    return [configFileInHomeDir,configFileInEtc,configFileInSubuserDir]
  
  def _expandPathsInConfig(self,config):
    """ Go through a freshly loaded config file and expand any environment variables in the paths. """
    subuserlib.loadMultiFallbackJsonConfigFile.expandPathsInDict(self.getUser().homeDir,["bin-dir","installed-programs.json","user-set-permissions-dir","program-home-dirs-dir"],config)
  
  def _loadConfig(self):
    """ Loads the subuser config: a dictionary of settings used by subuser. """
    configFileHierarchy = self._getSubuserConfigPaths()
    config = subuserlib.loadMultiFallbackJsonConfigFile.getConfig(configFileHierarchy)
    self._expandPathsInConfig(config)
    self.__config = config

  def __init__(self,user):
    super(subuserlib.classes.userOwnedObject.UserOwnedObject,self).__init__(user)
    self._loadConfig()

  def getBinDir(self):
    """ Get the directory where the executables for subusers are to be stored. """
    return self.__config["bin-dir"]

  def getRegistryPath(self):
    """ Get the path to the user's registry where subusers and installed docker images are registered. """
    return self.__config["registry-path"]

  def getInstalledImagesDotJsonPath(self):
    """ Get the path to the installed-images.json file where installed docker images are registered. """
    return os.path.join(self.getRegistryPath(),"installed-images.json")

  def getSubusersDotJsonPath(self):
    """ Get the path to the subusers.json file where subusers are registered. """
    return os.path.join(self.getRegistryPath(),"subusers.json")

  def getUserSetPermissionsDir(self):
    """ Get the path to the directory where user set, subuser specific, permissions are stored. """
    return self.__config["user-set-permissions-dir"]

  def getSubuserHomeDirsDir(self):
    """ Get the path to the directory where the home directories of each subuser are stored. """
    return self.__config["program-home-dirs-dir"]
    

