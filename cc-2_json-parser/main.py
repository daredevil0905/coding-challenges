"""
CODING CHALLENGE 2: Implement a JSON parser

In this challenge we need to implement a JSON parser that successfully parses a given JSON object
and it is also able to distinguish between a valid and invalid JSON representations.
The challenge can be found at: https://codingchallenges.fyi/challenges/challenge-json-parser
"""

# Import the necessary packages
import sys
import re

# define the Parser class
class Parser:

  def __init__(self, data="") -> None:
    self.data = data

  def __str__(self):
    return f"{self.data}"
  
  # Remove all the whitespaces in the input JSON object except those when they are within quotes
  def removeSpaces(self):

    # retrieve all the quoted strings in the data
    quotedStrings = re.findall(r'"([^"]*)"', self.data)

    # replace all whitespaces with '' in data
    self.data = re.sub(r'\s+', '', self.data)

    # retrieve the new quoted strings after whitespace replacement
    newQuotedStrings = re.findall(r'"([^"]*)"', self.data)

    # replace the new quoted strings with the original quoted strings that may/may not have contained whitespaces
    for idx in range(len(newQuotedStrings)):
      self.data = self.data.replace(newQuotedStrings[idx], quotedStrings[idx])
  
  # Check whether the data has proper opening and closing braces
  def checkOpeningAndClosingBraces(self) -> bool:
    return self.data[0] == "{" and self.data[-1] == "}" 

  # Check the (key, value) pairs recursively
  def checkKeyValuePairs(self):
    pass

  # Check JSON validity
  def checkJSONValidity(self) -> (bool, str):

    self.removeSpaces()

    if len(self.data) <= 1:
      return (False, "Length of input less than 2 non-whitespace characters")

    if not self.checkOpeningAndClosingBraces():
      return (False, "Input does not open with '{' or close with '}")
    
    self.data = self.data[1:-1]

    
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
  