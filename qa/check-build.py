"""Offline release gate: all local links, media and edition anchors must exist."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json

root=Path(__file__).resolve().parents[1]
out=root/'dist'
class Page(HTMLParser):
    def __init__(self,path):
        super().__init__()
        self.ids=set()
        self.refs=[]
        self.path=path
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self,tag,attrs):
        props=dict(attrs)
        if key:=props.get('id'):
            assert key not in self.ids,(self.path.name,key)
            self.ids.add(key)
        for key in ('src','href','poster'):
            if value:=props.get(key):self.refs.append(value)

pages={p:Page(p) for p in out.glob('*.html')}
assert len(pages)==7,len(pages)
for p,page in pages.items():
    for ref in page.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        path=(p.parent/unquote(u.path)).resolve() if u.path else p
        assert path.is_relative_to(out),ref
        assert path.is_file(),(p.name,ref)
        if u.fragment and path in pages:
            assert unquote(u.fragment) in pages[path].ids,(p.name,ref)
assert {'evidence','visual-lesson','nasa-date','map-retry'}<=pages[out/'atlas.html'].ids
assert 'v5.0' in (out/'index.html').read_text(encoding='utf-8')
assert len(json.loads((root/'content/history-v5.json').read_text(encoding='utf-8'))['timeline'])==9
assert (out/'media/creeds-24s.mp4').stat().st_size>10000
print('Verified seven generated pages, local assets, fragment links and V5 media.')

