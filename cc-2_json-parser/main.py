"""
CODING CHALLENGE 2: Implement a JSON parser

In this challenge we need to implement a JSON parser that successfully parses a given JSON object
and it is also able to distinguish between a valid and invalid JSON representations.
The challenge can be found at: https://codingchallenges.fyi/challenges/challenge-json-parser
"""

# Import the necessary packages
import sys
import re
from typing import Tuple

# define the Parser class
class Parser:

  PATTERN = {
    "QUOTED_STRING_PATTERN": r'"([^"]*)"',
    "WHITESPACE_PATTERN": r'\s+',
    "VALID_KEY_PATTERN": r'"([^"]+)":',
    "VALID_STRING_VALUE_PATTERN": r'"([^"]*)"',
    "VALID_NUMBER_VALUE_PATTERN": r'[+-]?\d+(\.\d+)?',
  }

  def __init__(self, data="") -> None:
    self.idx = 0
    self.data = data

  def __str__(self):
    return f"{self.data}"
  
  # Remove all the whitespaces in the input JSON object except those when they are within quotes
  def removeSpaces(self):

    # retrieve all the quoted strings in the data
    quotedStrings = re.findall(self.PATTERN["QUOTED_STRING_PATTERN"], self.data)

    # replace all whitespaces with '' in data
    self.data = re.sub(self.PATTERN["WHITESPACE_PATTERN"], '', self.data)

    # retrieve the new quoted strings after whitespace replacement
    newQuotedStrings = re.findall(self.PATTERN["QUOTED_STRING_PATTERN"], self.data)

    # replace the new quoted strings with the original quoted strings that may/may not have contained whitespaces
    for idx in range(len(newQuotedStrings)):
      self.data = self.data.replace(newQuotedStrings[idx], quotedStrings[idx])

  # Helper function to check pattern matching
  def matchPattern(self, pattern: str) -> Tuple[bool, str]:
    pattern = re.compile(pattern)
    match = re.search(pattern, self.data[self.idx:])
    if match and (match := match.group()) and self.data.startswith(match, self.idx):
      return (True, match)
    return (False, "")

  # Check the validity of key
  def checkValidKey(self) -> Tuple[bool, str]:
    return self.matchPattern(self.PATTERN["VALID_KEY_PATTERN"])

  # Check the validity of value
  def checkValidValue(self) -> Tuple[bool, str]:

    if self.data[self.idx] == '"':
      validity, value = self.matchPattern(self.PATTERN["VALID_STRING_VALUE_PATTERN"])
      if not validity:
        return (False, f"Invalid value at index {self.idx}")
      self.idx += len(value)
      return (True, value)
    
    elif '0' <= self.data[self.idx] <= '9':
      validity, value = self.matchPattern(self.PATTERN["VALID_NUMBER_VALUE_PATTERN"])
      if not validity:
        return (False, f"Invalid value at index {self.idx}")
      self.idx += len(value)
      return (True, value)
    
    elif self.data[self.idx] == '[':
      start = self.idx
      self.idx += 1
      typeOfValue = None

      while self.data[self.idx] != ']':

        validity, value = self.checkValidValue()

        if not validity or (typeOfValue != None and type(value) != typeOfValue):
          return (False, f"Invalid value at {self.idx}")
        
        typeOfValue = type(value) if not typeOfValue else None

        if self.data[self.idx] != ',' and self.data[self.idx] != ']':
          return (False, f"Invalid character: delimiter or end of array expected {self.idx}")
        
        self.idx += 1 if self.data[self.idx] == ',' else 0
        
      self.idx += 1
      return (True, self.data[start:self.idx])
    
    elif self.data[self.idx] == '{':
      return self.checkJSONValidity()
    
    elif self.data.startswith(('true', 'false', 'null'), self.idx):
      prefix = next((prefix for prefix in ('true', 'false', 'null') if self.data.startswith(prefix, self.idx)))
      self.idx += len(prefix)
      return (True, prefix)
    
    else:
      return (False, f"Incorrect value at {self.idx}")

  # Check JSON validity
  def checkJSONValidity(self) -> Tuple[bool, str]:

    self.removeSpaces()

    if len(self.data) <= 1:
      return (False, "Length of input less than 2 non-whitespace characters")
    
    if self.data[self.idx] != '{':
      return (False, f"JSON at {self.idx} does not start with" + '{')

    self.idx += 1
    
    while self.data[self.idx] != '}':
      # Check if the data string starts with ", followed by one or more characters, " and then a ':' indicating a valid key item
      
      validity, key = self.checkValidKey()
      if not validity:
        return (False, f"Invalid key at index {self.idx}, {self.data}")
      
      self.idx += len(key)

      validity, value = self.checkValidValue()
      if not validity:
        return (False, f"Invalid value at index {self.idx}: {value}")
      
      self.idx += 1 if self.data[self.idx] == ',' else 0

    return (True, "")


# JSON input function
def getJSONInput() -> str:
  print("Enter the JSON object to validate. Once the entire JSON is entered, go to a newline and then press Ctrl+D (or Ctrl+Z on Windows) to end response.")
  return sys.stdin.read()

# Main function
def main() -> int:
  # Get the JSON input
  jsonData = getJSONInput()

  # define the parser object
  parser = Parser(jsonData)
  
  validity, error = parser.checkJSONValidity()

  if validity:
    print("Valid JSON entered")
    return 0
  else:
    print(f"Invalid JSON entered: {error}")
    return 1

if __name__ == "__main__":
  
  exitCode = main()
  