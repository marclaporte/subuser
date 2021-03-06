#!/usr/bin/env python
# This file should be compatible with both Python 2 and 3.
# If it is not, please file a bug report.

#external imports
import os
#internal imports
#import ...

def isExecutable(fpath):
  """ Returns true if the given filepath points to an executable file. """
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

# Origonally taken from: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(image):
  fpath, fname = os.path.split(image)

  if not fpath == '':
    if isExecutable(image):
      return image
  else:
    def matchesImage(path):
      fpath,fname = os.path.split(path)
      return image == fname
    imageMatches = queryPATH(matchesImage)
    if len(imageMatches) > 0:
      return imageMatches[0]
   
  return None

def queryPATH(test):
  """ Search the PATH for an executable.

Given a function which takes an absoulte filepath and returns True when the filepath matches the query, return a list of full paths to matched files. """
  matches = []
  def appendIfMatches(exeFile):
    if isExecutable(exeFile):
      if test(exeFile):
        matches.append(exeFile)

  for path in os.environ["PATH"].split(os.pathsep):
    path = path.strip('"')
    if os.path.exists(path):
      for fileInPath in os.listdir(path):
        exeFile = os.path.join(path, fileInPath)
        appendIfMatches(exeFile)

  return matches
