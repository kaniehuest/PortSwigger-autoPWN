# AutoPWN for PortSwigger Labs

Scripts to automate attacks on PortSwigger Labs.\
**You don't need Burpsuite Professional.**

# usage

```console
$ python3 bsqli-1.py -h
This is the script for:
'Blind SQL injection with conditional responses'

Usage: python3 bsqli-1.py -u <url>
```

# List of Labs

| Scripts    | Labs                                                           |
| ---------- | -------------------------------------------------------------- |
| bsqli-1.py | Blind SQL injection with conditional responses                 |
| bsqli-2.py | Blind SQL injection with conditional errors                    |
| bsqli-3.py | Blind SQL injection with time delays                           |
| bsqli-4.py | Blind SQL injection with time delays and information retrieval |
| auth-1.py  | Username enumeration via different responses\*                 |
| auth-2.py  | Username enumeration via subtly different responses\*          |
| auth-3.py  | Username enumeration via response timing                       |
| auth-4.py  | Broken brute-force protection, IP block                        |
| auth-5.py  | Username enumeration via account lock                          |

Enjoy and have fun learning :)
