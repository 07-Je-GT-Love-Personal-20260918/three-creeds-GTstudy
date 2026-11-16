"""Evidence, storyboard and map controls for the fifth edition."""
from html import escape as E
import json

def enrich(root):
    path=root/'content/history-v5.json'
    data=json.loads(path.read_text(encoding='utf-8-sig')) if path.exists() else {}
    timeline=''.join(f'<li><strong>{E(x["year"])}</strong><div><b>{E(x["title"])}</b><p>{E(x["detail"])}</p></div></li>' for x in data.get('timeline',[]))
    chains=''.join(f'<details><summary>{E(x["title"])}</summary><dl><dt>圣经脉络</dt><dd>{E(x["bible"])}</dd><dt>圣约与救恩</dt><dd>{E(x["covenant"])}</dd><dt>教义界线</dt><dd>{E(x["guardrail"])}</dd><dt>闭卷回想</dt><dd>{E(x["recall"])}</dd></dl></details>' for x in data.get('chains',[]))
    sources=' · '.join(f'<a href="{E(x["url"])}" rel="noopener" target="_blank">{E(x["title"])} ↗</a>' for x in data.get('sources',[]))
    for file in (root/'dist').glob('*.html'):
        html=file.read_text(encoding='utf-8')
        html=html.replace('v4.0','v5.0').replace('2026.10.24','2026.11.14')
        html=html.replace('</head>','<link rel="stylesheet" href="v5.css"><script src="v5.js" defer></script></head>',1)
        if file.name in ('index.html','atlas.html'):
            html=html.replace('<option value="esri">Esri 全球街道图</option><option value="osm">OpenStreetMap 备选</option>',
                '<option value="auto">自动择源 · 推荐</option><option value="esri">Esri 街道</option><option value="osm">OpenStreetMap 街道</option><option value="topo">Esri 地形</option><option value="imagery">Esri 卫星影像</option><option value="nasa">NASA 近实时观测</option>')
            html=html.replace('<div id="modern-map" hidden','<div class="map-extra"><button type="button" id="map-retry" hidden>↻ 重试在线底图</button><label id="nasa-picker" hidden>观测日期（UTC） <input type="date" id="nasa-date"></label></div><div id="modern-map" hidden')
            html=html.replace('现代地图不是古代疆界，也不是实时卫星画面。任何在线服务都可能受地区网络影响；连接不佳时请切换服务或使用上方本地图。数据署名保留在地图内。',
                '现代街道和地形不代表古代疆界。Esri 影像是不同日期的拼接；NASA 为按日期发布的近实时观测，可能有云层和缺测。在线覆盖不等于每个网络都能连通，本地示意图可独立阅读。')
        if file.name=='atlas.html':
            html=html.replace('<a href="#culture">','<a href="#evidence">年代证据</a><a href="#visual-lesson">图解短片</a><a href="#culture">',1)
            panels=f'''<section id="evidence"><span class="micro-label">时间 · 地点 · 证据</span><h2>把会议、文本与传播分开读</h2><ol class="v5-timeline">{timeline}</ol>
            <h3>三份信经各自守护什么？</h3><div class="v5-compare" role="region" aria-label="三信经比较"><table><thead><tr><th>信经</th><th>面对的问题</th><th>记忆抓手</th></tr></thead><tbody>
            <tr><th scope="row">使徒</th><td>所信的福音如何在洗礼和教导中整体宣认？</td><td>父、子、圣灵；创造至复活。</td></tr>
            <tr><th scope="row">尼西亚</th><td>若子是受造者，敬拜他与靠他得救如何成立？</td><td>子非受造；圣灵也受敬拜。</td></tr>
            <tr><th scope="row">亚他那修</th><td>怎样同时守住一神、三个位格和基督的两性？</td><td>一体三位；一位两性。</td></tr></tbody></table></div>
            <div class="v5-chains">{chains}</div><p class="small">以下资料用于历史与教义解释；正式中文认信仍由 CCI 原典页核对。{sources}</p></section>
            <section id="visual-lesson"><span class="micro-label">短片 · 流程 · 回想</span><h2>从共同宣认，到划清界线</h2><div class="v5-film"><video controls playsinline preload="none" width="960" height="540" poster="media/creeds-poster.webp" aria-label="三信经二十四秒图解短片"><source src="media/creeds-24s.mp4" type="video/mp4"></video><div><h3>24 秒图解 · 无声字幕</h3><ol class="v5-flow"><li><b>罗马及拉丁西方</b>洗礼中的宣认</li><li><b>尼西亚与君士坦丁堡</b>澄清子与圣灵的神性</li><li><b>迦克墩及后来拉丁传统</b>区分一位两性与一体三位</li></ol><details><summary>短片文字版</summary><p>使徒信经承接早期洗礼认信。325 年尼西亚会议回答子是否受造；381 年与君士坦丁堡传统相关，451 年迦克墩会议保存了长式文本的见证，并说明基督两性。亚他那修信经则是后来的拉丁文本，作者不能按标题认定。</p></details></div></div></section>'''
            html=html.replace('<section id="culture">',panels+'<section id="culture">',1)
        if file.name=='index.html':
            html=html.replace('</div><div class="hero-collage"', '<a class="v5-trail-link" href="atlas.html#visual-lesson">▷ 24 秒图解与历史地图</a></div><div class="hero-collage"',1)
        html=html.replace('<div class="mark-style-grid">','''<div class="v5-presets" role="group" aria-label="记忆重点预设"><button type="button" data-preset="core">◆ 核心</button><button type="button" data-preset="distinction">≠ 分辨</button><button type="button" data-preset="review">↻ 待复习</button></div><p class="small">可组合样式，下划线颜色也可单独选择。</p><div class="mark-style-grid">''',1)
        html=html.replace('</select></label></div><p id="mark-style-preview"', '''</select></label><label>划线颜色 <select name="lineColor"><option value="">跟随标记色</option><option value="gold">金</option><option value="red">朱砂</option><option value="blue">深蓝</option><option value="green">青绿</option><option value="purple">紫</option></select></label></div><p id="mark-style-preview"''',1)
        html=html.replace('<div id="notes-list">','<label class="v5-note-filter">只看 <select id="notes-filter"><option value="">全部标记</option><option value="core">核心</option><option value="distinction">分辨</option><option value="review">待复习</option></select></label><div id="notes-list">',1)
        file.write_text(html,encoding='utf-8')

