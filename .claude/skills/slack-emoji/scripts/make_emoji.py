#!/usr/bin/env python3
"""슬랙 커스텀 이모지 생성기 (128x128, 128KB 이하).
사용: python3 make_emoji.py "텍스트" out.gif --anim shake --fg "#ffffff" --bg "#ff5a5f"
anim: none(PNG) | shake | bounce | blink | rainbow | spin
"""
import argparse, glob, math, colorsys
from PIL import Image, ImageDraw, ImageFont

S = 128

def font_path():
    for p in ["/usr/share/fonts/**/NanumGothicBold.ttf", "/usr/share/fonts/**/NotoSansCJK*Bold*",
              "/usr/share/fonts/**/wqy-zenhei.ttc", "/System/Library/Fonts/AppleSDGothicNeo.ttc",
              "C:/Windows/Fonts/malgunbd.ttf"]:
        h = glob.glob(p, recursive=True)
        if h: return h[0]
    return None

def fit_font(text, lines):
    fp = font_path()
    for size in range(110, 8, -2):
        f = ImageFont.truetype(fp, size) if fp else ImageFont.load_default()
        d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        w = max(d.textbbox((0, 0), l, font=f)[2] for l in lines)
        h = sum(d.textbbox((0, 0), l, font=f)[3] for l in lines)
        if w <= S - 12 and h <= S - 12: return f
    return f

def render(text, fg, bg, dx=0, dy=0, angle=0, scale=1.0):
    lines = text.split("\\n") if "\\n" in text else text.split("\n")
    f = fit_font(text, lines)
    img = Image.new("RGBA", (S, S), bg if bg else (0, 0, 0, 0))
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    hs = [d.textbbox((0, 0), l, font=f) for l in lines]
    total = sum(b[3] - b[1] for b in hs) + 4 * (len(lines) - 1)
    y = (S - total) / 2
    for l, b in zip(lines, hs):
        w = b[2] - b[0]
        d.text(((S - w) / 2 - b[0], y - b[1]), l, font=f, fill=fg,
               stroke_width=3, stroke_fill="black" if not bg else bg)
        y += b[3] - b[1] + 4
    if scale != 1.0:
        n = int(S * scale); layer = layer.resize((n, n)); c = Image.new("RGBA", (S, S)); c.paste(layer, ((S-n)//2, (S-n)//2)); layer = c
    if angle: layer = layer.rotate(angle, resample=Image.BICUBIC)
    img.alpha_composite(layer, (int(dx), int(dy)))
    return img

def main():
    a = argparse.ArgumentParser()
    a.add_argument("text"); a.add_argument("out")
    a.add_argument("--anim", default="none"); a.add_argument("--fg", default="#ffffff")
    a.add_argument("--bg", default="#ff5a5f", help="'none' = 투명")
    o = a.parse_args(); bg = None if o.bg == "none" else o.bg
    if o.anim == "none":
        render(o.text, o.fg, bg).save(o.out, optimize=True); return
    N = 12; frames = []
    for i in range(N):
        t = i / N
        if o.anim == "shake": fr = render(o.text, o.fg, bg, dx=6*math.sin(t*2*math.pi*2), angle=5*math.sin(t*2*math.pi))
        elif o.anim == "bounce": fr = render(o.text, o.fg, bg, dy=-12*abs(math.sin(t*math.pi)), scale=1-0.06*abs(math.cos(t*math.pi)))
        elif o.anim == "blink": fr = render(o.text, o.fg if i % 4 < 2 else "#ffd400", bg)
        elif o.anim == "rainbow":
            r, g, b = colorsys.hsv_to_rgb(t, 0.9, 1); fr = render(o.text, (int(r*255), int(g*255), int(b*255), 255), bg)
        elif o.anim == "spin": fr = render(o.text, o.fg, bg, angle=-360*t)
        else: raise SystemExit("unknown anim")
        frames.append(fr)
    pal = [f.convert("RGBA").quantize(colors=64, method=Image.FASTOCTREE) for f in frames]
    pal[0].save(o.out, save_all=True, append_images=pal[1:], duration=80, loop=0, disposal=2, optimize=True)

if __name__ == "__main__":
    main()
