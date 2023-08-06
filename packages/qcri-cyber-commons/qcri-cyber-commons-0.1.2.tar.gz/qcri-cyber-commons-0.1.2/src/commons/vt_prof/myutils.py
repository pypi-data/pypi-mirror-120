'''
Description: VT profile utility functions
Author: @nabeelxy
'''

import re
import string

def get_num(char):
  numbers = dict()
  numbers['0'] = "zero"
  numbers['1'] = "one"
  numbers['2'] = "two"
  numbers['3'] = "three"
  numbers['4'] = "four"
  numbers['5'] = "five"
  numbers['6'] = "six"
  numbers['7'] = "seven"
  numbers['8'] = "eight"
  numbers['9'] = "nine"
  return numbers[char]

def get_table_old(domain):
  pattern_char = re.compile("^[a-z]")
  pattern_digit = re.compile("^[0-9]")
  if (len(domain) > 0):
    lowerdomain = domain.lower()
  if (pattern_char.search(lowerdomain)):
    return lowerdomain[0] + "_vt"
  elif (pattern_digit.search(lowerdomain)):
    return get_num(lowerdomain[0]) +"_vt"
  else:
    return "special_vt"
#given the domain name, return the table name to use
def get_table(domain):
  pattern_char = re.compile("^[a-z]")
  pattern_digit = re.compile("^[0-9]")
  if (len(domain) > 0):
    lowerdomain = domain.lower()
    if (pattern_char.search(lowerdomain)):
      #alpha-numeric start
      second_level = "rest"
      if (len(domain) > 1 and string.ascii_lowercase.find(lowerdomain[1]) > -1):
        second_level = lowerdomain[1]

      return lowerdomain[0] + "_" + second_level + "_vt"
    elif (pattern_digit.search(lowerdomain)):
      second_level = "rest"
      if (len(domain) > 1 and string.digits.find(lowerdomain[1]) > -1):
        second_level = get_num(lowerdomain[1])

      return get_num(lowerdomain[0]) + "_" + second_level +"_vt"
    else:
      #special character start
      return "special_vt"

def get_cursor_key(domain):
  pattern_char = re.compile("^[a-z0-9]")
  if (len(domain) > 0):
    lowerdomain = domain.lower()
    if (pattern_char.search(lowerdomain)):
      second_key = "rest"
      if (len(domain) > 1 and pattern_char.search(lowerdomain[1]) and 
         ((string.ascii_lowercase.find(lowerdomain[0]) > -1 and string.ascii_lowercase.find(lowerdomain[1]) > -1) or 
         (string.digits.find(lowerdomain[0]) > -1 and string.digits.find(lowerdomain[1]) > -1))):
        second_key = lowerdomain[1]
      #alpha-numeric start
      return lowerdomain[0] + "_" + second_key
    else:
      #special character start
      return 'special'

def get_tables():
  tables = list()
  for char in string.ascii_lowercase:
    for char2 in string.ascii_lowercase:
      tables.append(char + "_" + char2 + "_vt")
    tables.append(char + "_rest" + "_vt")
  for dig in string.digits:
    for dig2 in string.digits:
      tables.append(get_num(dig) + "_" + get_num(dig2) + "_vt")
    tables.append(get_num(dig) + "_rest" + "_vt")
  tables.append("special_vt") 
  return tables

def get_prefixes_new():
  prefixes = list()
  for char in string.ascii_lowercase:
    for char2 in string.ascii_lowercase:
      prefixes.append(char + "_" + char2)
    prefixes.append(char + "_rest")
  for dig in string.digits:
    for dig2 in string.digits:
      prefixes.append(dig + "_" + dig2)
    prefixes.append(dig + "_rest")
  prefixes.append("special") 
  return prefixes 

def get_prefixes():
  prefixes = list()
  for char in string.ascii_lowercase:
    prefixes.append(char)
  for dig in string.digits:
    prefixes.append(get_num(dig))
  prefixes.append("special") 
  return prefixes 
