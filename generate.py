#!/usr/bin/env python3
"""Generate the 1024x1024 news front page for make.fun bounty
news-image-20261123: "Sum up 23 November's world news in one image".

Deterministic: no network, no randomness, no timestamps in the output.
Run:  python3 generate.py   (writes assets/entry.png)
The entry program (main.py) simply copies assets/entry.png to
$MAKEFUN_OUTPUT_DIR/entry.png, which the bounty brief explicitly allows:
"the simplest program copies an image the repository holds".

Stories (all verified from public reporting on 23 Nov 2026; see SOURCES.md):
  1. COP31 climate talks collapse in Antalya with no deal.
  2. Ukraine says naval drones sank a Russian warship off Benghazi, Libya.
  3. Nvidia reinstates Jensen Huang as chief executive.
  4. Belgium national strike grounds flights nationwide.
  5. IRGC says three tankers hit mines in the Strait of Hormuz.
  6. Democrats reach 258 House seats, largest majority since 1992.
Plus a ticker: Indonesia factory fire, India aid to Nepal, Pakistani astronaut.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets", "entry.png")

W = H = 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (178, 34, 34)
BLUE = (31, 78, 121)
TEAL = (14, 110, 110)
GOLD = (176, 124, 22)
LIGHT = (233, 226, 211)
GREY = (96, 96, 96)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(s):
    return font("DejaVuSerif-Bold.ttf", s)


def serif(s):
    return font("DejaVuSerif.ttf", s)


def sans_b(s):
    return font("DejaVuSans-Bold.ttf", s)


def sans(s):
    return font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_ship(d, x, y, s, col):
    d.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55),
               (x + s * 0.85, y + s * 0.85), (x + s * 0.15, y + s * 0.85)],
              fill=col)
    d.line([(x + s * 0.5, y + s * 0.55), (x + s * 0.5, y + s * 0.12)],
           fill=col, width=4)
    d.polygon([(x + s * 0.5, y + s * 0.14), (x + s * 0.82, y + s * 0.42),
               (x + s * 0.5, y + s * 0.42)], fill=col)
    for yy in (y + s * 0.92, y + s * 0.98):
        d.line([(x + 4, yy), (x + s - 4, yy)], fill=col, width=3)


def icon_chip(d, x, y, s, col):
    d.rectangle([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
                outline=col, width=4)
    d.rectangle([x + s * 0.4, y + s * 0.4, x + s * 0.6, y + s * 0.6],
                fill=col)
    for i in range(3):
        off = s * (0.32 + 0.18 * i)
        d.line([(x + off, y + s * 0.06), (x + off, y + s * 0.22)],
               fill=col, width=3)
        d.line([(x + off, y + s * 0.78), (x + off, y + s * 0.94)],
               fill=col, width=3)
        d.line([(x + s * 0.06, y + off), (x + s * 0.22, y + off)],
               fill=col, width=3)
        d.line([(x + s * 0.78, y + off), (x + s * 0.94, y + off)],
               fill=col, width=3)


def icon_plane(d, x, y, s, col):
    # simple side-view plane: fuselage, wing, tail, nose
    d.ellipse([x + s * 0.08, y + s * 0.38, x + s * 0.92, y + s * 0.62],
              fill=col)
    d.polygon([(x + s * 0.30, y + s * 0.42), (x + s * 0.55, y + s * 0.10),
               (x + s * 0.68, y + s * 0.10), (x + s * 0.58, y + s * 0.44)],
              fill=col)
    d.polygon([(x + s * 0.12, y + s * 0.40), (x + s * 0.22, y + s * 0.14),
               (x + s * 0.32, y + s * 0.14), (x + s * 0.28, y + s * 0.42)],
              fill=col)
    d.polygon([(x + s * 0.55, y + s * 0.58), (x + s * 0.72, y + s * 0.86),
               (x + s * 0.82, y + s * 0.86), (x + s * 0.68, y + s * 0.58)],
              fill=col)


def icon_tanker(d, x, y, s, col):
    d.rectangle([x + s * 0.08, y + s * 0.45, x + s * 0.92, y + s * 0.75],
                fill=col)
    d.rectangle([x + s * 0.14, y + s * 0.22, x + s * 0.30, y + s * 0.45],
                fill=col)
    d.line([(x + s * 0.05, y + s * 0.85), (x + s * 0.95, y + s * 0.85)],
           fill=col, width=3)
    d.line([(x + s * 0.05, y + s * 0.93), (x + s * 0.95, y + s * 0.93)],
           fill=col, width=3)
    # mine above the deck
    cx, cy, r = x + s * 0.62, y + s * 0.18, s * 0.10
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(cx + math.cos(a) * r, cy + math.sin(a) * r),
                (cx + math.cos(a) * (r + 7), cy + math.sin(a) * (r + 7))],
               fill=col, width=2)


def icon_capitol(d, x, y, s, col):
    # dome + columns
    d.pieslice([x + s * 0.28, y + s * 0.08, x + s * 0.72, y + s * 0.52],
               180, 360, fill=col)
    d.rectangle([x + s * 0.24, y + s * 0.50, x + s * 0.76, y + s * 0.58],
                fill=col)
    for i in range(4):
        cx = x + s * (0.30 + 0.13 * i)
        d.rectangle([cx - 4, y + s * 0.60, cx + 4, y + s * 0.82], fill=col)
    d.rectangle([x + s * 0.18, y + s * 0.82, x + s * 0.82, y + s * 0.90],
                fill=col)


ICONS = {"ship": icon_ship, "chip": icon_chip, "plane": icon_plane,
         "tanker": icon_tanker, "capitol": icon_capitol}

# ---------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

# ---- masthead
d.text((W // 2, 44), "THE WORLD IN ONE PAGE", font=serif_b(62),
       fill=INK, anchor="ma")
d.text((W // 2, 118), "MONDAY, 23 NOVEMBER 2026", font=sans_b(24),
       fill=RED, anchor="ma")
rule(d, 36, 152, W - 36, 3)
rule(d, 36, 158, W - 36, 1)

# ---- lead story: COP31
LX, LW = 36, 600
y = 182
d.text((LX, y), "CLIMATE  ·  ANTALYA, TURKEY", font=sans_b(21), fill=RED)
y += 34
y = draw_lines(d, LX, y,
               wrap(d, "COP31 COLLAPSES WITH NO DEAL", serif_b(54), LW),
               serif_b(54), INK, 58)
y += 10
y = draw_lines(
    d, LX, y,
    wrap(d, "After 44 hours of overtime, the EU and others reject "
            "a draft text that never names fossil fuels.",
         serif(25), LW),
    serif(25), INK, 32)
y += 8
d.text((LX, y), "Longest COP ever; first breakdown since 2009.",
       font=sans(21), fill=GREY)

# lead art: cracked globe, right side
AX, AY, AW, AH = 668, 178, 320, 268
d.rectangle([AX, AY, AX + AW, AY + AH], fill=BLUE)
cx, cy, r = AX + 150, AY + 120, 92
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 130, 170))
d.ellipse([cx - 52, cy - 78, cx + 18, cy - 18], fill=(96, 168, 92))
d.ellipse([cx - 78, cy + 8, cx - 8, cy + 62], fill=(96, 168, 92))
d.ellipse([cx + 28, cy + 28, cx + 88, cy + 88], fill=(96, 168, 92))
crack = [(cx - 88, cy - 96), (cx - 48, cy - 52), (cx - 66, cy - 12),
         (cx - 22, cy + 22), (cx - 44, cy + 62), (cx + 2, cy + 96)]
d.line(crack, fill=(255, 214, 64), width=6, joint="curve")
d.text((AX + AW // 2, AY + AH - 44), "NO DEAL IN ANTALYA",
       font=sans_b(22), fill=WHITE, anchor="ma")
rule(d, 36, 478, W - 36, 2)

# ---- section label
d.text((36, 492), "MORE FROM MONDAY", font=sans_b(22), fill=RED)
d.text((W - 36, 492), "23 NOV 2026", font=sans_b(22), fill=GREY, anchor="ra")

STORIES = [
    ("CONFLICT · LIBYA", "Ukraine drones hit Russian ships off Libya",
     "Kyiv says drones sank a corvette at Benghazi.",
     "ship", BLUE),
    ("TECH · SILICON VALLEY", "Nvidia brings back Jensen Huang as CEO",
     "Back days after resigning; Trump intervened.",
     "chip", GOLD),
    ("EUROPE · BELGIUM", "Belgium strike grounds flights nationwide",
     "Air traffic halted 07:00-21:00; ~430 flights axed.",
     "plane", RED),
    ("MIDDLE EAST · HORMUZ", "IRGC says tankers hit mines in Hormuz",
     "Three tankers caught fire under US escort, Iran claims.",
     "tanker", TEAL),
    ("POLITICS · USA", "Democrats hit 258 House seats",
     "Largest House majority since 1992.",
     "capitol", BLUE),
]

CW = (W - 72 - 16) // 2
CH, GAP = 138, 12
y0 = 524
for i, (kick, head, summ, icon, col) in enumerate(STORIES):
    row, c = divmod(i, 2)
    x = 36 + c * (CW + 16)
    y = y0 + row * (CH + GAP)
    d.rectangle([x, y, x + CW, y + CH], outline=INK, width=1)
    d.rectangle([x, y, x + 96, y + CH], fill=LIGHT)
    ICONS[icon](d, x + 12, y + 22, 72, col)
    tx = x + 112
    d.text((tx, y + 10), kick, font=sans_b(16), fill=RED)
    hy = draw_lines(d, tx, y + 32,
                    wrap(d, head, sans_b(22), CW - 128),
                    sans_b(22), INK, 27)
    draw_lines(d, tx, hy + 2,
               wrap(d, summ, sans(17), CW - 128), sans(17), GREY, 22)

# ticker box (6th cell)
x = 36 + CW + 16
y = y0 + 2 * (CH + GAP)
d.rectangle([x, y, x + CW, y + CH], fill=INK)
d.text((x + 16, y + 12), "ALSO TODAY", font=sans_b(16),
       fill=(255, 214, 64))
draw_lines(d, x + 16, y + 38,
           wrap(d, "24 killed in Indonesia factory fire, ~30 missing · "
                   "India gives $1.62bn aid to flood-hit Nepal · "
                   "China names a Pakistani astronaut for its space station",
                sans(19), CW - 32), sans(19), WHITE, 25)

# ---- footer
rule(d, 36, 972, W - 36, 1)
d.text((36, 982),
       "Compiled from public reporting, 23 Nov 2026: CNN · Reuters · AP · "
       "BusinessWorld · IRNA via Reuters",
       font=sans(14), fill=GREY)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
