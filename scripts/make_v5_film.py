"""Build an original silent motion graphic; no third-party footage."""
from pathlib import Path
import math,subprocess
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg

root=Path(__file__).resolve().parents[1]
out=root/'dist/media';out.mkdir(exist_ok=True)
font=Path('C:/Windows/Fonts/msyh.ttc')
if not font.exists(): font=Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
f=lambda n:ImageFont.truetype(str(font),n)
fonts={n:f(n) for n in (24,28,32,46,52)}
scenes=[
 ('01 · 洗礼认信','罗马与拉丁西方','使徒信经把创造、救赎与复活','连成可以在洗礼和教导中宣认的福音。','#54cbab'),
 ('02 · 会议与文本','325 → 381 → 451','尼西亚澄清子的神性；后来长式更明说圣灵。','迦克墩会议记录提供长式文本的见证。','#84baff'),
 ('03 · 分清而不分割','希腊语争辩与拉丁归纳','基督一位、两性；三一独一、三个位格。','亚他那修信经是后来的拉丁文本。','#eac178'),
 ('04 · 闭卷回想','三份文本，一个福音','使徒：宣认什么？  尼西亚：子是谁？','亚他那修：怎样分辨位格、本质和两性？','#dfa5fc')
]
def frame(t):
 i=min(3,int(t//6));small,title,l1,l2,c=scenes[i]
 im=Image.new('RGB',(960,540),'#102538');d=ImageDraw.Draw(im)
 for x,y,r in ((800,210,190),(825,210,146),(850,210,103)):
  y+=int(8*math.sin(t*.8));d.ellipse((x-r,y-r,x+r,y+r),outline='#29445e',width=2)
 d.rounded_rectangle((42,43,918,497),radius=28,outline='#41617b',width=2)
 d.text((72,72),small,font=fonts[28],fill=c)
 d.text((72,141),title,font=fonts[52],fill='#f4f8ff')
 d.text((72,254),l1,font=fonts[32],fill='#e3eff9')
 d.text((72,307),l2,font=fonts[32],fill='#e3eff9')
 for j in range(4):
  x=73+211*j;d.rounded_rectangle((x,423,x+189,430),radius=3,fill='#41617b')
  p=min(1,max(0,(t-j*6)/6))
  if p:d.rounded_rectangle((x,423,x+int(189*p),430),radius=3,fill=c)
 d.text((73,447),'GTstudy  /  三大信经图解',font=fonts[24],fill='#a8c7dc')
 return im
frame(0).save(out/'creeds-poster.webp',quality=82)
command=[imageio_ffmpeg.get_ffmpeg_exe(),'-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','960x540','-r','15','-i','-','-an','-c:v','libx264','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'creeds-24s.mp4')]
with subprocess.Popen(command,stdin=subprocess.PIPE) as proc:
 for j in range(360):proc.stdin.write(frame(j/15).tobytes())
 proc.stdin.close()
 if proc.wait(): raise SystemExit('video encoding failed')
print('Encoded 24-second diagram film')

