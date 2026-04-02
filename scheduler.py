import os
import urllib.request
import json

url = os.environ.get("SCRIPT_URL", "")
if url:
    with urllib.request.urlopen(url) as r:
        exec(r.read().decode())
else:
    print("SCRIPT_URL not set")
