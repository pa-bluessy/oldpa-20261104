from rank import *
import re,sys
b,S={'dp':(db,DS),'mw':(mb,MS)}[sys.argv[1]]
for s in sorted(b,key=lambda s:-b[s][0]['views']):
    print('##',s)
    for x in b[s][:5]:
      d=(x.get('desc') or '').replace('\n',' ')
      m=re.search(r'℗ ?\d{4}[^.]{0,50}',d); rel=re.search(r'Released on: ?\d{4}-\d\d-\d\d',d)
      al=x.get('album')
      if not al and 'desc' in x:
        mm=re.search(r'· [^·]+?  (.{1,60}?)  ℗',d); al='?'+(mm.group(1) if mm else '')
      print('   ',x['id'],x['views'],x['dur'],x['channel'][:14],'|',x['title'][:60],'| AL:',al,'|',m.group(0) if m else '', rel.group(0) if rel else '', '' if (x.get('album') or 'desc' not in x) else '| D:'+d[:220])
