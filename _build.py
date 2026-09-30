# キャンパスギア サイト生成スクリプト
# 使い方: このフォルダで「python3 _build.py」を実行すると、
# _src/ の記事から posts/・index.html・about.html・sitemap.xml を作り直します。
import json, re, glob, math, html as H
BASE = "https://sei627appple.github.io/campus-gear/"
SITE = "キャンパスギア"
GEAR = "M23.23 13.65 L25.96 13.81 L25.96 18.19 L23.23 18.35 L22.77 19.45 L24.59 21.50 L21.50 24.59 L19.45 22.77 L18.35 23.23 L18.19 25.96 L13.81 25.96 L13.65 23.23 L12.55 22.77 L10.50 24.59 L7.41 21.50 L9.23 19.45 L8.77 18.35 L6.04 18.19 L6.04 13.81 L8.77 13.65 L9.23 12.55 L7.41 10.50 L10.50 7.41 L12.55 9.23 L13.65 8.77 L13.81 6.04 L18.19 6.04 L18.35 8.77 L19.45 9.23 L21.50 7.41 L24.59 10.50 L22.77 12.55 Z M20.20 16 A4.2 4.2 0 1 0 11.80 16 A4.2 4.2 0 1 0 20.20 16 Z"
LOGO = f'<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#161616"/><path fill="#fff" fill-rule="evenodd" d="{GEAR}"/><circle cx="16" cy="16" r="2.2" fill="#f5c400"/></svg>'
CAT_ORDER = ["PC選び","Mac","PCトラブル","ガジェット","デザイン","大学生活"]

def head(title, desc, url, ogtitle, ogtype, root, active=''):
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{root}favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#ffffff">
<meta name="google-site-verification" content="px3PQoKTtbqM-c-VHl2T7kXuzPvQNFVLgsJrkCguZck">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="{ogtype}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{SITE}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}style.css">
</head>
<body>
<a class="skip" href="#main">本文へスキップ</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{root}" aria-label="{SITE} トップへ">{LOGO}<span class="brand-text"><span class="brand-ja">{SITE}</span><span class="brand-en">CAMPUS GEAR</span></span></a>
    <nav class="site-nav" aria-label="メインメニュー"><a class="nav-home" href="{root}"{' aria-current="page"' if active=='home' else ''}>記事一覧</a><a href="{root}about.html"{' aria-current="page"' if active=='about' else ''}>このブログについて</a></nav>
  </div>
</header>
'''
def foot(root, cats, extra_js=''):
    catlinks=''.join(f'<a href="{root}?cat={H.escape(c)}">{c}</a>' for c in cats)
    return f'''
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <a class="brand" href="{root}">{LOGO}<span class="brand-text"><span class="brand-ja">{SITE}</span><span class="brand-en">CAMPUS GEAR</span></span></a>
      <nav class="footer-cats" aria-label="カテゴリ">{catlinks}<a href="{root}about.html">このブログについて</a></nav>
    </div>
    <p>記事内のリンクには広告（アフィリエイトリンク）が含まれることがあります。</p>
    <p>&copy; 2026 {SITE}</p>
  </div>
</footer>
{extra_js}</body>
</html>
'''
def jdate(d): y,m,dd=d.split('-'); return f"{int(y)}年{int(m)}月{int(dd)}日"
def dot(d): return d.replace('-', '.')

posts=[]
for f in glob.glob('_src/*.html'):
    s=open(f).read()
    m=re.match(r'<!--META (\{.*?\}) -->\n', s, re.S)
    p=json.loads(m.group(1)); p['body']=s[m.end():]; posts.append(p)
posts.sort(key=lambda p:(p['date'], p['order']), reverse=True)
cats=[c for c in CAT_ORDER if any(p['cat']==c for p in posts)]+sorted({p['cat'] for p in posts}-set(CAT_ORDER))

TOTOP_JS='''<button class="to-top" type="button" aria-label="ページの上へ戻る"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
<script>
(function(){var b=document.querySelector('.to-top');if(!b)return;
function f(){b.classList.toggle('show',window.scrollY>600)}
window.addEventListener('scroll',f,{passive:true});f();
b.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'})});})();
</script>
'''

for i,p in enumerate(posts):
    url=BASE+f"posts/{p['slug']}.html"
    body=p['body']
    heads=[]
    def addid(m):
        heads.append(re.sub('<[^>]+>','',m.group(1)))
        return f'<h2 id="s{len(heads)}">{m.group(1)}</h2>'
    body=re.sub(r'<h2>(.*?)</h2>', addid, body)
    text=re.sub('<[^>]+>','',body)
    mins=max(1, math.ceil(len(re.sub(r'\s','',text))/500))
    toc=''
    if len(heads)>=3:
        toc='  <details class="toc" open>\n    <summary>目次</summary>\n    <ol>\n'+''.join(f'      <li><a href="#s{k+1}">{h}</a></li>\n' for k,h in enumerate(heads))+'    </ol>\n  </details>\n'
    newer = posts[i-1] if i>0 else None
    older = posts[i+1] if i+1<len(posts) else None
    pager='<nav class="pager" aria-label="前後の記事">'
    if older: pager+=f'<a class="prev" href="{older["slug"]}.html"><span class="label">← 前の記事</span>{older["title"]}</a>'
    if newer: pager+=f'<a class="next" href="{newer["slug"]}.html"><span class="label">次の記事 →</span>{newer["title"]}</a>'
    pager+='</nav>\n'
    others=[q for q in posts if q is not p and q is not newer and q is not older]
    rel=sorted(others, key=lambda q:(q['cat']!=p['cat'], q['order']))[:4]
    related='<section class="related" aria-labelledby="rel">\n  <h2 id="rel">あわせて読みたい</h2>\n  <ul>\n'+''.join(f'    <li><a href="{q["slug"]}.html">{q["title"]}</a></li>\n' for q in rel)+'  </ul>\n</section>\n'
    out=head(f"{p['title']} | {SITE}", p['description'], url, p['title'], 'article', '../')
    out+=f'''
<main id="main">
<div class="wrap">
<article>
  <nav class="crumbs" aria-label="現在地"><a href="../">ホーム</a><span>›</span><a href="../?cat={H.escape(p['cat'])}">{p['cat']}</a></nav>
  <p class="pr">※この記事にはプロモーションが含まれることがあります</p>
  <h1>{p['title']}</h1>
  <div class="article-meta"><span class="tag">{p['cat']}</span><time datetime="{p['date']}">{jdate(p['date'])}</time><span>約{mins}分で読めます</span></div>
{toc}  <div class="body">
{body.rstrip()}
  </div>
</article>
{pager}{related}</div>
</main>
'''+foot('../', cats, TOTOP_JS)
    open(f"posts/{p['slug']}.html",'w').write(out)

counts={c:sum(1 for p in posts if p['cat']==c) for c in cats}
chips='<button class="chip" type="button" data-cat="" aria-pressed="true">すべて<span class="n">'+str(len(posts))+'</span></button>'+''.join(f'<button class="chip" type="button" data-cat="{c}" aria-pressed="false">{c}<span class="n">{counts[c]}</span></button>' for c in cats)
items=''.join(f'''    <li data-cat="{p['cat']}" data-text="{H.escape((p['title']+' '+p['excerpt']+' '+p['cat']).lower())}"><a href="posts/{p['slug']}.html">
      <div class="post-meta"><span class="tag">{p['cat']}</span><time datetime="{p['date']}">{dot(p['date'])}</time></div>
      <div class="title">{p['title']}</div>
      <p class="excerpt">{p['excerpt']}</p>
    </a></li>
''' for p in posts)
INDEX_JS='''<script>
(function(){
var list=document.querySelectorAll('.post-list li'),chips=document.querySelectorAll('.chip'),
    q=document.getElementById('q'),empty=document.querySelector('.empty'),count=document.querySelector('.result-count');
var cat=new URLSearchParams(location.search).get('cat')||'';
function apply(){
  var t=q.value.trim().toLowerCase(),n=0;
  list.forEach(function(li){var ok=(!cat||li.dataset.cat===cat)&&(!t||li.dataset.text.indexOf(t)>-1);li.hidden=!ok;if(ok)n++;});
  chips.forEach(function(c){c.setAttribute('aria-pressed',c.dataset.cat===cat?'true':'false')});
  empty.hidden=n>0; count.textContent=(cat||t)?n+'件の記事':'';
  var u=new URL(location.href); if(cat)u.searchParams.set('cat',cat); else u.searchParams.delete('cat'); history.replaceState(null,'',u);
}
chips.forEach(function(c){c.addEventListener('click',function(){cat=c.dataset.cat;apply();})});
q.addEventListener('input',apply); apply();
})();
</script>
'''
idx=head(f"{SITE}｜大学生のPC・ガジェット・デザインのメモ", "PCやガジェット、デザインが好きな大学生が、パソコン選びや便利な使い方、デザインのことを書いているブログです。", BASE, SITE, 'website', '', 'home')
idx+=f'''
<main id="main">
<div class="wrap">
  <div class="hero">
    <h1>大学生のPC・ガジェット・デザインのメモ</h1>
    <p>パソコンの選び方や便利な使い方、レポートや発表で使えるちょっとしたコツを書いています。</p>
  </div>
  <div class="tools">
    <label class="search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg><input id="q" type="search" placeholder="記事をさがす（例：PDF、バックアップ）" aria-label="記事を検索"></label>
    <div class="chips" role="group" aria-label="カテゴリで絞り込み">{chips}</div>
  </div>
  <p class="result-count" aria-live="polite"></p>
  <ul class="post-list">
{items}  </ul>
  <p class="empty" hidden>条件に合う記事が見つかりませんでした。</p>
</div>
</main>
'''+foot('', cats, INDEX_JS)
open('index.html','w').write(idx)

about=head(f"このブログについて | {SITE}", "キャンパスギアの運営者情報、広告、プライバシーポリシー、免責事項について。", BASE+"about.html", "このブログについて", 'website', '', 'about')
about+='''
<main id="main">
<div class="wrap">
<article>
  <nav class="crumbs" aria-label="現在地"><a href="./">ホーム</a><span>›</span>このブログについて</nav>
  <h1>このブログについて</h1>
  <div class="body">
  <p>キャンパスギアは、PCやガジェット、デザインが好きな大学生が書いているブログです。パソコンの選び方や便利な使い方、レポートや発表で使えるちょっとしたコツなど、大学生活で役に立ちそうなことを書いています。</p>
  <p>内容の間違いや、わかりにくいところがあれば直していきます。</p>
  <h2>広告について</h2>
  <p>このブログでは、Amazonアソシエイトや楽天アフィリエイトなどのアフィリエイトプログラムを利用して、商品やサービスを紹介することがあります。紹介しているリンクから商品が購入されると、運営者に報酬が入ることがあります。広告を含む記事には、その旨を記載しています。</p>
  <h2>プライバシーポリシー</h2>
  <p>今後、アクセス解析ツールや広告配信サービスを使う場合があります。これらのサービスは、個人を特定しない形でCookieを使ってアクセス情報を集めることがあります。Cookieはブラウザの設定で無効にできます。使うサービスが決まったら、このページに追記します。</p>
  <h2>免責事項</h2>
  <p>できるだけ正確な情報を書くようにしていますが、内容が正しいこと、最新であることを保証するものではありません。価格や仕様、キャンペーンなどは変わることがあるので、購入や申し込みの前には公式の情報を確認してください。このブログの情報を使ったことで生じた損害については、責任を負いかねます。</p>
  <h2>著作権</h2>
  <p>文章や画像の無断転載はご遠慮ください。</p>
  </div>
</article>
</div>
</main>
'''+foot('', cats)
open('about.html','w').write(about)

sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm+=f'  <url><loc>{BASE}</loc></url>\n  <url><loc>{BASE}about.html</loc></url>\n'
sm+=''.join(f"  <url><loc>{BASE}posts/{p['slug']}.html</loc><lastmod>{p['date']}</lastmod></url>\n" for p in posts)
sm+='</urlset>\n'
open('sitemap.xml','w').write(sm)
print(len(posts),'posts built;', cats)
