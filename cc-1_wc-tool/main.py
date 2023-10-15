# Implement the 'wc' unix tool which stands for 'word count'. It can count number of lines,
# words and characters and this is my Python implementation of the same
# This coding challenge can be found at: https://codingchallenges.fyi/challenges/challenge-wc

import os
import sys

# Helper functions

def printResults(results):
  for result in results:
    print(result)

# Step One: In this step your goal is to write a simple version of wc,
# let's call it ccwc (cc for Coding Challenges) that takes the command line option -c
# and outputs the number of bytes in a file.

def getBytes(paths: list) -> (list):
  results, totalBytes = [], 0
  for path in paths:
    try:
      byteSize = os.stat(path).st_size
    except FileNotFoundError:
      raise FileNotFoundError(f"Path {path} does not exist or is inaccessible")
    results.append(f"{byteSize} {path}")
    totalBytes += byteSize
  if len(paths) == 1:
    return results
  results.append(f"{totalBytes} total")
  return results

# < ---------------------------------------------------------------------------------------- >

# Step Two: In this step your goal is to support the command line option -l
# that outputs the number of lines in a file.

def getLines(paths: list) -> str:
  results, totalLines = [], 0
  for path in paths:
    try:
      fileHandle = open(path, 'r', encoding="utf8")
    except FileNotFoundError:
      raise FileNotFoundError(f"Path {path} does not exist or is inaccessible")
    lineCount = 0
    for _ in fileHandle:
      lineCount += 1
    results.append(f"{lineCount} {path}")
    totalLines += lineCount
  if len(paths) == 1:
    return results
  results.append(f"{totalLines} total")
  return results

# < ---------------------------------------------------------------------------------------- >

# Step Three: In this step your goal is to support the command line option -w
# that outputs the number of words in a file.

def getWords(paths: list) -> str:
  results, totalWords = [], 0
  for path in paths:
    try:
      fileHandle = open(path, 'r', encoding="utf8")
    except FileNotFoundError:
      raise FileNotFoundError(f"Path {path} does not exist or is inaccessible")
    wordCount = 0
    for line in fileHandle:
      wordCount += len(line.split())
    results.append(f"{wordCount} {path}")
    totalWords += wordCount
  if len(paths) == 1:
    return results
  results.append(f"{totalWords} total")
  return results

# < ---------------------------------------------------------------------------------------- >

# Step Four: In this step your goal is to support the command line option -m
# that outputs the number of characters in a file.

def getCharacters(paths: list) -> str:
  results, totalCharacters = [], 0
  for path in paths:
    try:
      fileHandle = open(path, 'r', encoding="utf8")
    except FileNotFoundError:
      raise FileNotFoundError(f"Path {path} does not exist or is inaccessible")
    charCount = len(fileHandle.read())
    results.append(f"{charCount} {path}")
    totalCharacters += charCount
  if len(paths) == 1:
    return results
  results.append(f"{totalCharacters} total")
  return results

# < ---------------------------------------------------------------------------------------- >

# Step Five: In this step your goal is to support the default option - 
# i.e. no options are provided, which is the equivalent to the -c, -l and -w options.

def getAll(paths: list) -> str:
  results = []
  totalCount = [0, 0, 0]
  for path in paths:
    linesResponse = int(getLines([path])[0].split()[0])
    wordsResponse = int(getWords([path])[0].split()[0])
    bytesResponse = int(getBytes([path])[0].split()[0])
    if os.path.exists(path) == False:
      raise FileNotFoundError(f"Path {path} does not exist or is inaccessible")
    results.append(f"{linesResponse} {wordsResponse} {bytesResponse} {path}")
    totalCount = [totalItemCount + itemCount for totalItemCount, itemCount in zip(totalCount, [linesResponse, wordsResponse, bytesResponse])]
  if len(paths) == 1:
    return results
  results.append(f"{totalCount[0]} {totalCount[1]} {totalCount[2]} total")
  return results
    

if __name__ == "__main__":

  cliInput = input('>')

  if cliInput.startswith('ccwc'):

    cliInput = cliInput.split()
    
    if len(cliInput) < 2:
      sys.exit("Not enough arguments passed")
    
    if cliInput[1] == '-c':
      printResults(getBytes(cliInput[2:]))
    elif cliInput[1] == '-l':
      printResults(getLines(cliInput[2:]))
    elif cliInput[1] == '-w':
      printResults(getWords(cliInput[2:]))
    elif cliInput[1] == '-m':
      printResults(getCharacters(cliInput[2:]))
    elif cliInput[1].startswith('-'):
      sys.exit("Incorrect option")
    else:
      printResults(getAll(cliInput[1:]))
  
  else:

    cliInput = cliInput.split('|')

    if len(cliInput) < 2:
      sys.exit("Not enough arguments passed")
    
    checkFilesPos = 1
    for i in range(1,len(cliInput)):
      if cliInput[i].strip().startswith('ccwc'):
        checkFilesPos = i - 1
        break
    
    files = cliInput[checkFilesPos].split()[1:]

    # Get option for ccwc
    cliInput = cliInput[checkFilesPos + 1].split()
    if len(cliInput) == 1:
      printResults(getAll(files))
    if cliInput[1] == '-c':
      printResults(getBytes(files))
    elif cliInput[1] == '-l':
      printResults(getLines(files))
    elif cliInput[1] == '-w':
      printResults(getWords(files))
    elif cliInput[1] == '-m':
      printResults(getCharacters(files))
    elif cliInput[1].startswith('-'):
      sys.exit("Incorrect option")
