import json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
YT="/workspace/ytvenv/bin/yt-dlp"
def s(q,n=10):
    r=subprocess.run([YT,"--flat-playlist","-j",f"ytsearch{n}:{q}"],capture_output=True,text=True,timeout=120)
    out=[]
    for l in r.stdout.splitlines():
        try:d=json.loads(l)
        except:continue
        out.append(dict(q=q,id=d.get('id'),title=d.get('title'),channel=d.get('channel'),views=d.get('view_count'),dur=d.get('duration')))
    return out
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
n=int(sys.argv[3]) if len(sys.argv)>3 else 10
res=[]
with ThreadPoolExecutor(12) as ex:
    for o in ex.map(lambda q:s(q,n),qs): res+=o
json.dump(res,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(res))
