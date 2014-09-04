#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import sys,os,getpass,subprocess,tempfile
#internal imports
import subuserlib.subprocessExtras

def getRecursiveDirectoryContents(directory):
  files = []
  for (directory,_,fileList) in os.walk(directory):
    for file in fileList:
      files.append(os.path.join(directory,file))
  return files

def getBasicFlags(subuserToRun):
  return [
    "-i",
    "-t",
    "--rm"]

def getPermissionFlagDict(subuserToRun):
  """
  This is a dictionary mapping permissions to functions which when given the permission's values return docker run flags. 
  """
  return {
   "allow-network-access" : lambda p: ["--net=bridge"] if p else ["--net=none"],
   "system-dirs" : lambda systemDirs: ["-v="+systemDir+":"+systemDir+":ro" for systemDir in systemDirs],
   "user-dirs" : lambda userDirs : ["-v="+os.path.join(subuserToRun.getUser().homeDir,userDir)+":"+os.path.join("/userdirs/",userDir)+":rw" for userDir in userDirs],
   "inherit-working-directory" : lambda p: ["-v="+cwd+":/pwd:rw","--workdir=/pwd"] if p else ["--workdir="+subuserToRun.getDockersideHome()],
   "stateful-home" : lambda p : ["-v="+subuserToRun.getHomeDirOnHost()+":"+subuserToRun.getDockersideHome()+":rw","-e","HOME="+subuserToRun.getDockersideHome()] if p else [],
   "x11" : lambda p: ["-e","DISPLAY=unix"+os.environ['DISPLAY'],"-v=/tmp/.X11-unix:/tmp/.X11-unix:rw"] if p else [],
   "graphics-card" : lambda p: ["--device=/dev/dri/"+device for device in os.listdir("/dev/dri")] if p else [],
   "sound-card" : lambda p: ["--device="+device for device in getRecursiveDirectoryContents("/dev/snd")] if p else [],
   "webcam" : lambda p: ["--device=/dev/"+device for device in os.listdir("/dev/") if device.startswith("video")] if p else [],
   "privileged" : lambda p: ["--privileged"] if p else [],
   "as-root" : lambda root: ["--user=0"] if root else ["--user="+str(os.getuid())]
   }

def getCommand(subuserToRun, programArgs):
  flags = getBasicFlags(subuserToRun)
  permissionFlagDict = getPermissionFlagDict(subuserToRun)
  permissions = subuserToRun.getPermissions()
  for permission, flagGenerator in permissionFlagDict.iteritems():
    flags.extend(flagGenerator(permissions[permission]))

  return ["run"]+flags+[subuserToRun.getImageId()]+[subuserToRun.getPermissions()["executable"]]+programArgs

def getPrettyCommand(subuserToRun,programArgs):
  """
  Get a command for pretty printing for use with dry-run.
  """
  command = getCommand(subuserToRun,programArgs)
  return "docker '"+"' '".join(command)+"'"

def run(subuserToRun,programArgs):
  def setupSymlinks():
    symlinkPath = os.path.join(subuserToRun.getHomeDirOnHost(),"Userdirs")
    destinationPath = "/userdirs"
    if not os.path.exists(symlinkPath):
      try:
        os.makedirs(subuserToRun.getHomeDirOnHost())
      except OSError:
        pass
      try:
        os.symlink(destinationPath,symlinkPath) #Arg, why are source and destination switched?
      #os.symlink(where does the symlink point to, where is the symlink)
      #I guess it's to be like cp...
      except OSError:
        pass

  if subuserToRun.getPermissions()["stateful-home"]:
    setupSymlinks()

  subuserToRun.getUser().getDockerDaemon().execute(getCommand(subuserToRun,programArgs))
