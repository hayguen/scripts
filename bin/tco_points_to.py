#!/usr/bin/env python3

import sys
import urllib3

if len(sys.argv) < 2:
    print("missing URL https://t.co/.. argument")
    print(f"usage: {sys.argv[0]} <short_url>")
    print("check https://redirectsniffer.com/ for a web UI")
    sys.exit(0)

shorturl = sys.argv[1]

for redir in [False, True]:
    print(f"\nGET with{'' if redir else 'out'} redirections:")
    response = urllib3.request("GET", shorturl, decode_content=False, redirect=redir)
    if response:
        print(f"status code:        {response.status}")
        print(f"redirect location:  {response.get_redirect_location()}")
        print(f"URL                 {response.geturl()}")
    else:
        print("no result")
