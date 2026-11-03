import json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
YT="/workspace/ytvenv/bin/yt-dlp"
def f(i):
    r=subprocess.run([YT,"-j","--skip-download","--no-warnings","https://www.youtube.com/watch?v="+i],capture_output=True,text=True,timeout=180)
    try:d=json.loads(r.stdout)
    except: return dict(id=i,err=r.stderr[-300:])
    return dict(id=i,title=d.get('title'),channel=d.get('channel'),views=d.get('view_count'),dur=d.get('duration'),desc=(d.get('description') or '')[:1500],album=d.get('album'),track=d.get('track'),artists=d.get('artists') or d.get('artist'),release_year=d.get('release_year'),upload=d.get('upload_date'))
ids=[l.strip() for l in open(sys.argv[1]) if l.strip()]
with ThreadPoolExecutor(10) as ex: res=list(ex.map(f,ids))
json.dump(res,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(res),sum('err' in r for r in res))
