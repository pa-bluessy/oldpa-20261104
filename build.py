import json,re,html,sys
sys.path.insert(0,'.')
from data import P1,P2
from rank import DP,MW,db,mb
M={**DP,**MW}
M['3pVQj2v7tBI'].update(dur=340,views=1619144)  # 単体で再取得した値
e=html.escape
def mmss(s): return f"{s//60}:{s%60:02d}"
def hms(s): return f"{s//3600}:{s%3600//60:02d}:{s%60:02d}"
def link(label,url): return f'<a href="{e(url)}">{e(label)}</a><span class="url">{e(url)}</span>'
def top(b):
  R=[];used=set()
  for s in b:
    for x in b[s]:
      if x['id'] not in used: used.add(x['id']);R.append((s,x));break
  R.sort(key=lambda t:-t[1]['views']);return R[:50]
def part(P,label,time,artist,genre,intro):
  ids=[];out=[];cum=0;n=0;names=set()
  for ch,title,narr,songs in P:
    out.append(f'<section class="ch"><div class="chhead"><span class="tag">{e(ch)}</span><h3>{e(title)}</h3></div><p class="narr">{e(narr)}</p>')
    for vid,name,src,desc in songs:
      m=M[vid];d=m['dur'];v=m['views'];cum+=d;n+=1;ids.append(vid)
      u=f"https://www.youtube.com/watch?v={vid}"
      out.append(f'<div class="song"><div class="row1"><span class="no">{n:02d}</span><span class="st">{e(name)}</span></div>'
        f'<div class="meta"><span class="tag">{mmss(d)}</span><span class="tag">再生 {v:,} 回</span><span class="tag">累計 {hms(cum)}</span></div>'
        f'<p class="src">音源：{e(src)}</p><p class="desc">{e(desc)}</p><p class="lk">{link("YouTubeで聴く",u)}</p></div>')
    out.append('</section>')
  pt="https://www.youtube.com/watch_videos?video_ids="+",".join(ids[:50])
  head=(f'<p class="kicker">{e(label)}　{e(time)}</p><h2>{e(artist)} <span class="g">— {e(genre)}</span></h2>'
        f'<p class="intro">{e(intro)}</p><div class="sum"><span class="tag">{n} 曲</span><span class="tag">合計 {hms(cum)}</span></div>'
        f'<p class="lk play">{link("このパートを曲順どおり続けて再生",pt)}</p>')
  return head+"".join(out),n,cum,pt,ids
intro1=("1968年、ロンドン。クラシックを学んだオルガン弾きと、きげんの悪い天才ギタリストが、同じバンドにいました。"
 "メンバーが入れかわるたびに「第1期」「第2期」「第3期」と呼ばれ、そのたびに音の色が変わっていく。"
 "スイスの湖のほとりで起きた火事、10分間の叫び、そして一度別れた5人の再会。"
 "第一部の1時間は、ハードロックの「元祖」のひとつ、ディープ・パープルの物語です。")
intro2=("ミシシッピの綿畑で、生ギターを弾いていた男がいました。本名はマッキンリー・モーガンフィールド。"
 "1943年にシカゴへ出た彼は、ギターに電気を通し、バンドを組み、「シカゴ・ブルース」という音を作りあげます。"
 "その音にあこがれたイギリスの若者たちが、のちにローリング・ストーンズやレッド・ツェッペリンになりました。"
 "1983年に亡くなるまでの40年を、2時間でたどります。主役は、マディ・ウォーターズ。")
h1,n1,t1,pt1,ids1=part(P1,"第一部","22:00–23:00","Deep Purple","HARD ROCK",intro1)
h2,n2,t2,pt2,ids2=part(P2,"第二部","23:00–25:00（翌1:00）","Muddy Waters","CHICAGO BLUES",intro2)
bridge=('<section class="bridge"><p class="kicker">22:59　つなぎ</p><h3>ハーモニカの音をたどって</h3>'
 '<p class="narr">第一部の最後の「Lazy」で鳴っていた、ブルースのはねるリズムと、ハーモニカ。'
 'イギリスのハードロックの人たちが若いころに夢中で聴いていたのが、海の向こう、シカゴのブルースでした。'
 'ここからは、大きな音を少しずつほどいて、その「おおもと」へさかのぼっていきます。灯りを落として、第二部へどうぞ。</p></section>')
def table(rows,setids,setnames,live_note):
  r=[]
  for i,(s,m) in enumerate(rows,1):
    u=f"https://www.youtube.com/watch?v={m['id']}"
    if m['id'] in setids: mk=' <span class="tag">今夜のセットリスト</span>'
    elif s in setnames: mk=' <span class="tag">今夜は別の版で</span>'
    else: mk=''
    t=re.sub(r"^(Deep Purple|DEEP PURPLE|Muddy Waters)\s*[-|]\s*","",m['title'])
    t=re.sub(r"^DEEP PURPLE \| ","",t)
    nt=''
    if live_note and m['channel']=='MUDDYWATERSVEVO' and '(Live)' in m['title']:
      nt='<br><span class="dim">※いつ・どこの演奏か書かれていないライブ音源（出典要確認）</span>'
    r.append(f'<li><span class="no">{i:02d}</span> {e(t)}{mk}<br><span class="dim">{mmss(m["dur"])} ／ {m["views"]:,} 回 ／ {e(m["channel"])}</span>{nt}<br>{link("動画",u)}</li>')
  return "<ol class='rank'>"+"".join(r)+"</ol>"
def setnames(P,b):
  ids={s[0] for c in P for s in c[3]}
  return ids,{k for k,v in b.items() if any(x['id'] in ids for x in v)}
i1,s1=setnames(P1,db);i2,s2=setnames(P2,mb)
DR=top(db);MR=top(mb)
gloss=('<section class="gloss"><h3>ことばのメモ</h3><ul>'
 '<li><b>第1期・第2期・第3期（Mk I／Mk II／Mk III）</b>：ディープ・パープルはメンバーがよく入れかわったので、時期ごとに「マーク1、2、3」と番号で呼ばれます。いちばん有名なのは、イアン・ギランが歌う第2期です。</li>'
 '<li><b>リフ</b>：曲の中で何度もくり返される、短いギターなどのフレーズ。</li>'
 '<li><b>シャッフル</b>：「タッタ、タッタ」とはねるリズム。ブルースによく使われます。</li>'
 '<li><b>スライドギター</b>：ビンの首や金属の筒を指にはめて、弦の上をすべらせて弾くやり方。泣いているような音が出ます。</li>'
 '<li><b>シカゴ・ブルース</b>：南部から北の大都市シカゴに移った人たちが、電気ギター・ハーモニカ・ピアノ・ドラムで演奏したブルース。マディはその中心人物です。</li>'
 '<li><b>チェス（Chess）</b>：シカゴのレコード会社。マディの1950年代のヒットはほとんどここから出ました（はじめは「アリストクラット」という名前）。</li>'
 '<li><b>スタジオ版</b>：録音スタジオで作った、レコードやCDに入っている音。</li>'
 '<li><b>リマスター</b>：昔の録音を、今の機械で聴きやすく整え直したもの。演奏そのものは同じです。</li>'
 '<li><b>公式配信音源（Topic）</b>：レコード会社がYouTubeに出している音源。「〜 - Topic」という名前のチャンネルに自動で並びます。</li>'
 '<li><b>公式MV</b>：公式チャンネルが出しているミュージックビデオ。</li>'
 '<li><b>公式ライブ盤</b>：コンサートの録音を、正式にレコードやCDとして発売したもの。</li>'
 '<li><b>カバー</b>：ほかの人が先に発表した曲を、自分たちで演奏すること。</li>'
 '<li><b>℗（マルピー）</b>：その録音の権利の年。発売年とずれることがあります。</li>'
 '<li><b>要確認</b>：たしかな出典がまだ見つかっていないところ。事実として言い切らないでください。</li></ul></section>')
css="""
:root{--bg:#0b1222;--card:#111a2e;--line:#1d2a44;--tx:#b9c2d3;--hd:#d3d9e4;--dim:#77839b;--ac:#c9a46a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.8 -apple-system,"Hiragino Sans","Hiragino Kaku Gothic ProN",sans-serif;-webkit-text-size-adjust:100%}
.wrap{max-width:680px;margin:0 auto;padding:28px 16px 60px}
h1{font-family:"Hiragino Mincho ProN",serif;color:var(--ac);font-weight:500;font-size:28px;margin:0;letter-spacing:.06em}
h2{font-family:"Hiragino Mincho ProN",serif;font-weight:500;font-size:24px;margin:4px 0 8px;color:var(--hd)}h2 .g{color:var(--ac);font-size:15px}
h3{font-size:17px;margin:0;color:var(--hd);font-weight:600}
.kicker{color:var(--ac);font-size:13px;letter-spacing:.12em;margin:0}
.narr{color:#a7b0c2;font-size:15px}
.tag{display:inline-block;border:1px solid var(--ac);color:var(--ac);border-radius:999px;padding:0 10px;font-size:12px;line-height:22px;margin:0 6px 6px 0;background:none}
.tabs{position:sticky;top:0;z-index:5;display:flex;gap:8px;background:var(--bg);padding:10px 0;margin-top:18px;border-bottom:1px solid var(--line)}
.tab{flex:1;background:none;border:1px solid var(--line);color:var(--tx);border-radius:10px;padding:8px 6px;font:inherit;font-size:14px;line-height:1.4;cursor:pointer}
.tab small{display:block;color:var(--dim);font-size:11px}
.tab[aria-selected="true"]{border-color:var(--ac);color:var(--ac)}
.panel{padding-top:16px}.panel[hidden]{display:none}
.ch{margin:26px 0 8px}.chhead{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.chhead .tag{margin:0}
.song{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:10px 0}
.row1{display:flex;gap:10px;align-items:baseline}.no{color:var(--dim);font-variant-numeric:tabular-nums;font-size:13px}.st{font-weight:600;color:var(--hd)}
.meta{margin-top:6px}.src{margin:2px 0;color:var(--dim);font-size:13px}.desc{margin:4px 0;font-size:15px}
a{color:var(--ac);text-decoration:underline;text-underline-offset:3px}
.url{display:block;color:var(--dim);font-size:11px;word-break:break-all;line-height:1.4}
.lk{margin:6px 0 0;font-size:14px}.play{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.bridge,.gloss,.note,.flow{margin-top:24px;padding:16px;border:1px solid var(--line);border-radius:12px;background:var(--card)}
details{margin-top:14px;border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--card)}summary{color:var(--ac);cursor:pointer}
.rank{list-style:none;padding:0;font-size:14px}.rank li{padding:8px 0;border-bottom:1px solid var(--line)}.dim{color:var(--dim)}
ul{padding-left:18px}footer{margin-top:40px;color:var(--dim);font-size:12px;text-align:center}
.tonext{margin-top:20px;text-align:center}.tonext button{background:none;border:1px solid var(--ac);color:var(--ac);border-radius:999px;padding:6px 16px;font:inherit;font-size:14px}
"""
note=('<section class="note"><h3>このページについて</h3><ul>'
 '<li>再生回数と長さは、2026年11月3日（火）日本時間の午前10時ごろに yt-dlp（YouTubeの情報を読み取る道具）で測った数字です。今は少し変わっているかもしれません。</li>'
 '<li>セットリストに使ったのは、公式チャンネルのスタジオ録音（公式配信音源・公式MV）と、正式に発売されたライブ盤（Muddy Waters at Newport 1960）だけです。ファンのアップロードや、非公式のライブ映像は入れていません。</li>'
 '<li>トップ50は、曲ごとに公式チャンネルでいちばん再生されている動画を1本選び、再生回数の順に並べた参考表です。テレビ出演やライブの映像もふくみます。フルアルバム、メドレー、ほかの人のカバー、20分をこえる動画は外しました。セットリストには、トップ50に入っていない渋めの曲（You Shook Me、My Home Is in the Delta など）もわざと混ぜています。</li>'
 '<li>Muddy Waters の公式VEVOチャンネルには「(Live)」とだけ書かれた、いつどこの演奏かわからない動画が多くあります。トップ50には「出典要確認」と書いてのせましたが、セットリストには入れていません。</li>'
 '<li>「Mannish Boy」の動画には、どのアルバムの音か書かれていません。長さ（5分29秒）から『Hard Again』（1977）の版と考えていますが、要確認です。「Perfect Strangers」の公式MVの音がスタジオ版と同じかも要確認です。</li>'
 '<li>年は、アルバムの発売年か、音源に書かれた ℗ の年です。はっきりしない場合は「要確認」と書いています。</li>'
 '<li>日本で再生できるかは、作成した環境からは確かめられていません（要確認）。YouTubeの「続けて再生」は、国や年齢確認の都合で一部の曲が飛ばされることがあります。</li></ul></section>')
js="""<script>
(function(){var tabs=document.querySelectorAll('.tab');
function show(id,scroll){tabs.forEach(function(t){var on=t.dataset.t===id;t.setAttribute('aria-selected',on);document.getElementById(t.dataset.t).hidden=!on});
 if(history.replaceState)history.replaceState(null,'','#'+id);if(scroll)document.querySelector('.tabs').scrollIntoView({behavior:'smooth'});}
tabs.forEach(function(t){t.addEventListener('click',function(){show(t.dataset.t,false)})});
document.querySelectorAll('[data-go]').forEach(function(b){b.addEventListener('click',function(){show(b.dataset.go,true)})});
var h=location.hash.slice(1);show(h==='muddy'?'muddy':'dp',false);})();
</script>"""
page=f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0b1222"><title>ざ・おーるど・ぱー 2026年11月4日（水）</title><style>{css}</style></head><body><div class="wrap">
<p class="kicker">音声ルーム on Gravity</p><h1>ざ・おーるど・ぱー</h1><p>2026年11月4日（水）日本時間<br>第一部 22:00–23:00　Deep Purple — HARD ROCK<br>第二部 23:00–翌1:00　Muddy Waters — CHICAGO BLUES</p>
<div><span class="tag">第一部 {n1}曲 {hms(t1)}</span><span class="tag">第二部 {n2}曲 {hms(t2)}</span></div>
<section class="flow"><h3>今夜の流れ</h3><p class="narr">22時、イギリスのハードロック、ディープ・パープルの1時間で幕をあけます。大きなオルガンとギターの音が、最後はブルースのハーモニカに行き着く。23時からは、その音の「ふるさと」、シカゴ・ブルースのマディ・ウォーターズへ。ロックの親をたずねて、時間を少しずつさかのぼる夜です。</p></section>
<nav class="tabs" role="tablist"><button class="tab" role="tab" data-t="dp">第一部 Deep Purple<small>22:00–23:00</small></button><button class="tab" role="tab" data-t="muddy">第二部 Muddy Waters<small>23:00–翌1:00</small></button></nav>
<div class="panel" id="dp" role="tabpanel">{h1}
{bridge}
<details><summary>Deep Purple 再生回数トップ50（参考）</summary>{table(DR,i1,s1,False)}</details>
<p class="tonext"><button data-go="muddy">第二部 Muddy Waters へ →</button></p></div>
<div class="panel" id="muddy" role="tabpanel" hidden>{h2}
<details><summary>Muddy Waters 再生回数トップ50（参考）</summary>{table(MR,i2,s2,True)}</details>
<p class="tonext"><button data-go="dp">← 第一部 Deep Purple へ</button></p></div>
{gloss}{note}
<footer>ざ・おーるど・ぱー　on Gravity</footer></div>{js}</body></html>"""
open('index.html','w').write(page)
print(n1,hms(t1),n2,hms(t2),len(DR),len(MR));print(pt1);print(pt2)
print('not in top50:',[i for i in ids1 if i not in {x['id'] for s,x in DR}],[i for i in ids2 if i not in {x['id'] for s,x in MR}])
