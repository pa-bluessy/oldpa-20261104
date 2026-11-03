import json,re
def load(fs):
    M={}
    for f in fs:
        try: L=json.load(open(f))
        except FileNotFoundError: continue
        for x in L:
            if 'err' in x: continue
            if x['id'] in M and 'desc' in M[x['id']] and 'desc' not in x: continue
            M[x['id']]=x
    return M
def norm(t): t=(t or '').lower().replace("’","'").replace("'","").replace("‘",""); return re.sub(r"[^a-z0-9]+"," ",t).strip()
def songs(qf,pre):
    S=[]
    for l in open(qf):
        l=l.strip()
        if not l or re.search(r"Made in Japan|official|Plantation|Newport|Folk Singer|Hard Again$|Live at Mister|Electric Mud$",l): continue
        s=l[len(pre):].strip()
        if s not in S: S.append(s)
    return S
def build(M,S,okch,bad,alias={}):
    B={}
    for s in S:
        ns=norm(alias.get(s,s))
        for x in M.values():
            c=x.get('channel') or ''
            if not okch(c) or not x.get('dur') or x['dur']>1200 or not x.get('views'): continue
            t=x['title'] or ''
            if bad and re.search(bad,t,re.I): continue
            nt=norm(t)
            if not re.search(r"(^| )"+re.escape(ns)+r"( |$)",nt): continue
            B.setdefault(s,[]).append(x)
    for s in B: B[s].sort(key=lambda x:-x['views'])
    return B
DPOK=lambda c: c in ('Deep Purple Official','earMUSIC') or c in ('Deep Purple - Topic','Glenn Hughes - Topic')
DPBAD=r"Celebrating Jon Lord|Ian Gillan|Track By Track|Behind The Scenes|Trailer|Rehearsal|MTV|Medley|Full Album|Glenn Hughes"
MWOK=lambda c: c in ('Muddy Waters - Topic','MUDDYWATERSVEVO','Muddy Waters')
MWBAD=r"Full Album|Medley|Rolling Stones|Remix"
DP=load(['dp_raw.json','dp_raw2.json','full_all.json','err_full.json','full_new.json'])
MW=load(['mw_raw.json','mw_raw2.json','mw_raw3.json','full_all.json','err_full.json','full_new.json','err_full2.json','full_all.json','err_full.json'])
DS=songs('dp_q.txt','Deep Purple');MS=songs('mw_q.txt','Muddy Waters')
db=build(DP,DS,DPOK,DPBAD,{'Gypsy':'The Gypsy'});mb=build(MW,MS,MWOK,MWBAD,{'Champagne and Reefer':'Champagne','Got My Mojo Working':'Mojo','Can\'t Lose What You Ain\'t Never Had':'Lose What You','Feel So Good':'Feel So Good','Mad Love':'Mad Love','Little Girl':'Little Girl'})
if __name__=='__main__':
  import sys
  for name,b,S in (('DP',db,DS),('MW',mb,MS)):
    print('=====',name,len(S),'songs; found',len(b),'missing',[s for s in S if s not in b])
    for s in sorted(b,key=lambda s:-b[s][0]['views']):
        print('##',s)
        for x in b[s][:6]: print('   ',x['id'],x['views'],x['dur'],x['channel'],'|',x['title'])
