#!/usr/bin/env python3
"""
Gelou Açaí Hero Banner Generator
1200×400px — Púrpura Tropical aesthetic
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H = 1200, 400
img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
draw = ImageDraw.Draw(img)

# ── Brand palette ─────────────────────────────────────────────────────────────
DEEP_PURPLE   = (74,  31, 117)   # #4A1F75
MED_PURPLE    = (107, 53, 160)   # #6B35A0
SKY_BLUE      = (135, 190, 220)  # #87BEDC
GREEN         = (125, 194, 107)  # #7DC26B
CREAM         = (255, 245, 230)
DARK_BAND     = (40,  15,  70)
BERRY_RED     = (140,  30,  70)
BERRY_DARK    = ( 90,  10,  45)
LIGHT_PURPLE  = (160, 100, 210)
GRANOLA       = (195, 155,  90)
GRANOLA_DARK  = (160, 115,  55)
WHITE         = (255, 255, 255)
DRIZZLE       = (220, 180, 240)

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_DIR = "/Users/Noel/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/f4ba2fd0-838e-46bb-8a5f-929678e5d123/b5b1f080-d038-4d3e-aa21-27f75efc4388/skills/canvas-design/canvas-fonts"

def load_font(name, size):
    try:
        return ImageFont.truetype(f"{FONT_DIR}/{name}", size)
    except:
        return ImageFont.load_default()

font_gelou     = load_font("Boldonse-Regular.ttf", 128)
font_acai      = load_font("Outfit-Bold.ttf", 54)
font_tagline   = load_font("WorkSans-Bold.ttf", 17)
font_contact   = load_font("BricolageGrotesque-Bold.ttf", 15)
font_delivery  = load_font("Outfit-Bold.ttf", 15)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. BACKGROUND GRADIENT  (deep → medium purple, left → right)
# ═══════════════════════════════════════════════════════════════════════════════
bg = Image.new("RGBA", (W, H))
bg_draw = ImageDraw.Draw(bg)
for x in range(W):
    t = x / W
    r = int(DEEP_PURPLE[0] + (MED_PURPLE[0] - DEEP_PURPLE[0]) * t)
    g = int(DEEP_PURPLE[1] + (MED_PURPLE[1] - DEEP_PURPLE[1]) * t)
    b = int(DEEP_PURPLE[2] + (MED_PURPLE[2] - DEEP_PURPLE[2]) * t)
    bg_draw.line([(x, 0), (x, H - 60)], fill=(r, g, b, 255))
# darker strip from y=340 to y=400
for y in range(H - 60, H):
    t2 = (y - (H - 60)) / 60
    r = int(MED_PURPLE[0] * (1 - t2) + DARK_BAND[0] * t2)
    g2= int(MED_PURPLE[1] * (1 - t2) + DARK_BAND[1] * t2)
    b = int(MED_PURPLE[2] * (1 - t2) + DARK_BAND[2] * t2)
    bg_draw.line([(0, y), (W, y)], fill=(r, g2, b, 255))
img = Image.alpha_composite(img, bg)
draw = ImageDraw.Draw(img)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. SUBTLE BACKGROUND SCATTER DOTS
# ═══════════════════════════════════════════════════════════════════════════════
random.seed(42)
scatter_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(scatter_layer)

dot_configs = [
    # (x, y, r, color, alpha)
    (950, 60,  22, LIGHT_PURPLE, 35),
    (1050, 120, 14, SKY_BLUE, 25),
    (1130, 50,  9,  LIGHT_PURPLE, 30),
    (1160, 200, 18, DEEP_PURPLE, 50),
    (1080, 300, 12, SKY_BLUE, 20),
    (880,  30,  7,  WHITE, 18),
    (820, 380,  5,  WHITE, 15),
    (160, 200, 30, DEEP_PURPLE, 40),
    (100,  80, 12, LIGHT_PURPLE, 25),
    (200,  40,  6, WHITE, 20),
    (300, 360, 18, DEEP_PURPLE, 45),
    (440, 380,  8, SKY_BLUE, 20),
    (700,  25, 10, WHITE, 15),
    (750, 380,  6, LIGHT_PURPLE, 25),
]
for (dx, dy, dr, dc, da) in dot_configs:
    col = (*dc[:3], da)
    sd.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=col)

# add tiny random dots
for _ in range(55):
    dx = random.randint(80, W-50)
    dy = random.randint(10, H-70)
    dr = random.randint(2, 5)
    da = random.randint(12, 30)
    col_choice = random.choice([WHITE, LIGHT_PURPLE, SKY_BLUE])
    sd.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=(*col_choice, da))

img = Image.alpha_composite(img, scatter_layer)
draw = ImageDraw.Draw(img)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. GREEN VERTICAL ACCENT BAR (left edge)
# ═══════════════════════════════════════════════════════════════════════════════
bar_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bd = ImageDraw.Draw(bar_layer)
# main bar
bd.rectangle([0, 0, 10, H - 60], fill=(*GREEN, 255))
# subtle glow alongside
for i in range(1, 8):
    alpha = int(80 * (1 - i/8))
    bd.rectangle([10, 0, 10+i, H - 60], fill=(*GREEN, alpha))
img = Image.alpha_composite(img, bar_layer)
draw = ImageDraw.Draw(img)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. LEFT TEXT — "gelou" + "açaí"
# ═══════════════════════════════════════════════════════════════════════════════
# Shadow for "gelou"
tx, ty = 38, 55
for sx, sy in [(-3,3),(3,3),(0,4),(-2,2)]:
    draw.text((tx+sx, ty+sy), "gelou", font=font_gelou, fill=(30, 5, 55, 180))

draw.text((tx, ty), "gelou", font=font_gelou, fill=WHITE)

# "açaí" in sky blue
ax, ay = 42, 200
# subtle shadow
draw.text((ax+2, ay+2), "açaí", font=font_acai, fill=(30, 5, 55, 140))
draw.text((ax, ay), "açaí", font=font_acai, fill=SKY_BLUE)

# ═══════════════════════════════════════════════════════════════════════════════
# 5. AÇAÍ BOWL ILLUSTRATION  (center, x=480–720, y=30–340)
# ═══════════════════════════════════════════════════════════════════════════════
bowl_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bl = ImageDraw.Draw(bowl_layer)

CX, CY = 600, 220   # bowl center

# ── bowl body ──────────────────────────────────────────────────────────────────
# outer bowl — dark gradient ellipse (widest)
for i in range(18, 0, -1):
    t  = i / 18
    rr = int(BERRY_DARK[0]*t + DEEP_PURPLE[0]*(1-t))
    gg = int(BERRY_DARK[1]*t + DEEP_PURPLE[1]*(1-t))
    bb = int(BERRY_DARK[2]*t + DEEP_PURPLE[2]*(1-t))
    bw = 115 + i*2
    bh = 70  + i*1
    bl.ellipse([CX-bw, CY-bh, CX+bw, CY+bh], fill=(rr, gg, bb, 255))

# inner bowl highlight
bl.ellipse([CX-90, CY-50, CX+90, CY+50], fill=(100, 40, 140, 255))

# ── rim highlight ──────────────────────────────────────────────────────────────
bl.arc([CX-115, CY-70, CX+115, CY+70], start=200, end=340,
       fill=(180, 130, 220, 180), width=4)

# ── açaí base filling (dark purple pool inside bowl) ──────────────────────────
for i in range(8):
    t = i/8
    rr = int(80*(1-t) + 50*t)
    gg = int(20*(1-t) + 10*t)
    bb = int(110*(1-t) + 80*t)
    bw = 88 - i*3
    bh = 42 - i*2
    bl.ellipse([CX-bw, CY-bh, CX+bw, CY+bh], fill=(rr, gg, bb, 255))

# ── bowl bottom taper ─────────────────────────────────────────────────────────
# polygon trapezoid for tapered bottom
pts = [
    (CX-100, CY+50),
    (CX+100, CY+50),
    (CX+30,  CY+140),
    (CX-30,  CY+140),
]
bl.polygon(pts, fill=(55, 15, 80, 255))
# shade on taper left
pts_l = [(CX-100, CY+50),(CX-30, CY+50),(CX-30, CY+140),(CX-50, CY+140)]
# fill with gradient manually
for yi in range(CY+50, CY+140):
    t = (yi - (CY+50)) / 90
    aa = int(120*(1-t))
    bl.line([(CX-100+(yi-(CY+50))*0.6, yi),(CX-90+(yi-(CY+50))*0.5, yi)],
            fill=(30,5,50,aa))

# ── TOPPINGS ───────────────────────────────────────────────────────────────────

# granola base layer — chunky blobs across the top of the açaí
granola_pts = [
    (CX-75, CY-30), (CX-55, CY-42), (CX-35, CY-25),
    (CX-15, CY-38), (CX+5,  CY-30), (CX+25, CY-40),
    (CX+50, CY-28), (CX+70, CY-36), (CX+85, CY-22),
]
for gx, gy in granola_pts:
    gr = random.randint(-4, 4)
    gc = GRANOLA if random.random() > 0.4 else GRANOLA_DARK
    bl.ellipse([gx-7+gr, gy-5+gr, gx+7+gr, gy+5+gr], fill=(*gc, 230))
    # small chunk
    bl.ellipse([gx+8, gy+2, gx+14, gy+8], fill=(*GRANOLA, 200))

# drizzle lines — honey/white drizzle
drizzle_pts = [
    [(CX-60, CY-50), (CX-30, CY-25), (CX,    CY-35), (CX+30, CY-20)],
    [(CX+20, CY-55), (CX+50, CY-30), (CX+75, CY-40)],
    [(CX-80, CY-30), (CX-55, CY-15), (CX-35, CY-22)],
]
for pts_drz in drizzle_pts:
    for i in range(len(pts_drz)-1):
        x1, y1 = pts_drz[i]
        x2, y2 = pts_drz[i+1]
        bl.line([(x1, y1),(x2, y2)], fill=(*DRIZZLE, 200), width=2)
        # dot at each point
        bl.ellipse([x1-2, y1-2, x1+2, y1+2], fill=(*DRIZZLE, 220))

# ── açaí berries ──────────────────────────────────────────────────────────────
berry_positions = [
    (CX-68, CY-58, 14), (CX-42, CY-65, 16), (CX-20, CY-60, 13),
    (CX+5,  CY-68, 15), (CX+30, CY-62, 14), (CX+55, CY-58, 16),
    (CX+75, CY-50, 12), (CX-80, CY-45, 11), (CX+90, CY-38, 10),
    (CX-50, CY-80, 12), (CX+10, CY-82, 13), (CX+55, CY-78, 11),
]
for bx, by, br in berry_positions:
    # berry body gradient
    for ri in range(br, 0, -1):
        t = ri / br
        rr = int(BERRY_RED[0]*t + BERRY_DARK[0]*(1-t))
        gg = int(BERRY_RED[1]*t + BERRY_DARK[1]*(1-t))
        bb = int(BERRY_RED[2]*t + BERRY_DARK[2]*(1-t))
        bl.ellipse([bx-ri, by-ri, bx+ri, by+ri], fill=(rr, gg, bb, 255))
    # highlight
    bl.ellipse([bx-br//3, by-br//2, bx, by-br//4], fill=(220, 130, 160, 160))
    # stem dot
    bl.ellipse([bx-2, by-br-2, bx+2, by-br+2], fill=(80, 40, 20, 200))

# ── strawberry slice ──────────────────────────────────────────────────────────
# ellipse slice at CX-30, CY-88
slx, sly = CX - 28, CY - 90
bl.ellipse([slx-12, sly-8, slx+12, sly+8], fill=(220, 60, 80, 240))
# seeds
for sx, sy in [(slx-4, sly-2),(slx+3, sly-4),(slx+1, sly+3)]:
    bl.ellipse([sx-1, sy-1, sx+1, sy+1], fill=(255, 220, 180, 220))
# leaves at top
bl.polygon([(slx, sly-8),(slx-5, sly-18),(slx+5, sly-18)], fill=(GREEN[0]-20, GREEN[1], GREEN[2], 220))

# ── banana slice (cream ellipse) ──────────────────────────────────────────────
bnx, bny = CX + 60, CY - 85
bl.ellipse([bnx-14, bny-7, bnx+14, bny+7], fill=(*CREAM, 230))
bl.ellipse([bnx-10, bny-4, bnx+10, bny+4], fill=(245, 228, 170, 220))

# ── coconut shavings ──────────────────────────────────────────────────────────
shaving_pts = [
    (CX-55, CY-100), (CX-20, CY-108), (CX+15, CY-105),
    (CX+45, CY-100),
]
for sx, sy in shaving_pts:
    bl.ellipse([sx-9, sy-3, sx+9, sy+3], fill=(*CREAM, 180))
    # slight angle by tiny rotation approximation
    bl.ellipse([sx-7, sy-2, sx+7, sy+2], fill=(240, 235, 220, 160))

# ── granola cluster overflow ───────────────────────────────────────────────────
for _ in range(14):
    gx = random.randint(CX-90, CX+90)
    gy = random.randint(CY-110, CY-55)
    gs = random.randint(4, 9)
    gc = random.choice([GRANOLA, GRANOLA_DARK, (210, 170, 100)])
    bl.ellipse([gx-gs, gy-gs//2, gx+gs, gy+gs//2], fill=(*gc, 200))

# ── bowl inner rim glow ────────────────────────────────────────────────────────
bl.arc([CX-88, CY-48, CX+88, CY+48], start=190, end=350,
       fill=(160, 100, 200, 100), width=3)

# ── bowl shine/reflection ─────────────────────────────────────────────────────
bl.arc([CX-100, CY-60, CX+100, CY+60], start=215, end=325,
       fill=(255, 255, 255, 60), width=5)

img = Image.alpha_composite(img, bowl_layer)
draw = ImageDraw.Draw(img)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. RIGHT SIDE — AÇAÍ BERRY CLUSTER + LEAF ACCENTS
# ═══════════════════════════════════════════════════════════════════════════════
right_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(right_layer)

# ── branch/stem ───────────────────────────────────────────────────────────────
branch_pts = [(950, 320),(960, 260),(980, 200),(1010, 150),(1040, 110),(1070, 80)]
for i in range(len(branch_pts)-1):
    x1,y1 = branch_pts[i]
    x2,y2 = branch_pts[i+1]
    rd.line([(x1,y1),(x2,y2)], fill=(70,35,20,200), width=4)

# ── açaí berry cluster (right side) ───────────────────────────────────────────
cluster = [
    # (x, y, r)
    (980, 190, 18), (1005, 175, 20), (1030, 165, 17),
    (960, 210, 14), (1015, 200, 15), (1045, 180, 16),
    (990, 225, 13), (1035, 210, 14), (1060, 195, 13),
    (970, 165, 12), (1055, 160, 11), (1070, 175, 12),
    (1000, 155, 10), (1025, 145, 13), (980, 240, 10),
    (1050, 225, 10), (1015, 235, 11), (935,  200, 10),
    (945, 225, 9),  (1075, 160, 9),
]
for bx, by, br in cluster:
    for ri in range(br, 0, -1):
        t = ri / br
        rr = int(BERRY_RED[0]*t + BERRY_DARK[0]*(1-t))
        gg = int(BERRY_RED[1]*t + BERRY_DARK[1]*(1-t))
        bb_v = int(BERRY_RED[2]*t + BERRY_DARK[2]*(1-t))
        rd.ellipse([bx-ri, by-ri, bx+ri, by+ri], fill=(rr, gg, bb_v, 255))
    # specular highlight
    rd.ellipse([bx-br//3, by-br//2, bx, by-br//5],
               fill=(230, 140, 170, 140))

# ── small second cluster (upper right) ────────────────────────────────────────
cluster2 = [
    (1090, 90, 13),(1110, 80, 15),(1130, 75, 12),(1105, 100, 11),
    (1125, 95, 10),(1145, 88, 11),(1115, 115, 9),(1140, 108, 10),
    (1095, 115, 8),(1155, 100, 9),
]
for bx, by, br in cluster2:
    for ri in range(br, 0, -1):
        t = ri / br
        rr = int(BERRY_RED[0]*t + BERRY_DARK[0]*(1-t))
        gg = int(BERRY_RED[1]*t + BERRY_DARK[1]*(1-t))
        bb_v = int(BERRY_RED[2]*t + BERRY_DARK[2]*(1-t))
        rd.ellipse([bx-ri, by-ri, bx+ri, by+ri], fill=(rr, gg, bb_v, 255))
    rd.ellipse([bx-br//3, by-br//2, bx, by-br//5],
               fill=(230, 140, 170, 120))

# ── tropical leaf accents ──────────────────────────────────────────────────────
def draw_leaf(draw_obj, tip_x, tip_y, base_x, base_y, width, color, alpha=210):
    """Draw a stylized tropical leaf."""
    dx = base_x - tip_x
    dy = base_y - tip_y
    length = math.hypot(dx, dy)
    if length == 0: return
    nx, ny = -dy/length, dx/length  # normal
    pts = [
        (tip_x, tip_y),
        (tip_x + dx*0.3 + nx*width, tip_y + dy*0.3 + ny*width),
        (base_x + nx*width*0.3, base_y + ny*width*0.3),
        (base_x, base_y),
        (base_x - nx*width*0.3, base_y - ny*width*0.3),
        (tip_x + dx*0.3 - nx*width, tip_y + dy*0.3 - ny*width),
    ]
    pts_int = [(int(x),int(y)) for x,y in pts]
    draw_obj.polygon(pts_int, fill=(*color, alpha))
    # midrib
    draw_obj.line([(tip_x, tip_y),(base_x, base_y)],
                  fill=(max(0,color[0]-30), max(0,color[1]-30), max(0,color[2]-30), 180), width=2)

LEAF_G = GREEN
LEAF_DG = (85, 155, 68)

# large leaves bottom-right area
draw_leaf(rd, 1080, 330, 1190, 270, 22, LEAF_G)
draw_leaf(rd, 1100, 350, 1195, 310, 18, LEAF_DG)
draw_leaf(rd, 1050, 355, 1160, 310, 20, LEAF_G, alpha=190)

# leaves behind cluster
draw_leaf(rd, 920, 150, 870, 100, 18, LEAF_DG, alpha=160)
draw_leaf(rd, 900, 180, 850, 120, 15, LEAF_G, alpha=140)

# upper-right corner leaf
draw_leaf(rd, 1150, 30, 1195, 80, 14, LEAF_G, alpha=170)
draw_leaf(rd, 1130, 20, 1185, 60, 12, LEAF_DG, alpha=150)

# ── decorative circular ring accent ───────────────────────────────────────────
# soft ring behind cluster
for thickness in range(6, 0, -1):
    alpha = int(60 * (1 - thickness/6))
    rd.arc([990-50-thickness, 190-50-thickness, 990+50+thickness, 190+50+thickness],
           start=0, end=360, fill=(*LIGHT_PURPLE, alpha), width=1)

img = Image.alpha_composite(img, right_layer)
draw = ImageDraw.Draw(img)

# ═══════════════════════════════════════════════════════════════════════════════
# 7. BOTTOM STRIP — dark band with text
# ═══════════════════════════════════════════════════════════════════════════════
strip_layer = Image.new("RGBA", (W, H), (0,0,0,0))
sd2 = ImageDraw.Draw(strip_layer)

# bottom dark band
sd2.rectangle([0, H-60, W, H], fill=(*DARK_BAND, 245))

# left green bar continues into strip
sd2.rectangle([0, H-60, 10, H], fill=(*GREEN, 255))

# separator line
sd2.line([(0, H-60),(W, H-60)], fill=(*LIGHT_PURPLE, 60), width=1)

# contact text — left-aligned, after bar
contact_str = "@geloubji  ·  (22) 99958-5490"
sd2.text((28, H-42), contact_str, font=font_contact, fill=(*SKY_BLUE, 230))

# delivery text — right side
delivery_str = "✦  ENTREGA GRÁTIS NA REGIÃO  ✦"
bbox = sd2.textbbox((0,0), delivery_str, font=font_delivery)
tw = bbox[2] - bbox[0]
sd2.text((W - tw - 30, H-42), delivery_str, font=font_delivery, fill=(*GREEN, 230))

# center dot separator
sd2.ellipse([W//2-3, H-37, W//2+3, H-31], fill=(*LIGHT_PURPLE, 160))

img = Image.alpha_composite(img, strip_layer)
draw = ImageDraw.Draw(img)

# ═══════════════════════════════════════════════════════════════════════════════
# 8. FINAL REFINEMENTS — glow halo behind bowl, overall warm vignette
# ═══════════════════════════════════════════════════════════════════════════════
glow = Image.new("RGBA", (W, H), (0,0,0,0))
gd = ImageDraw.Draw(glow)
# soft radial glow behind bowl
for r in range(180, 0, -1):
    alpha = int(18 * (1 - r/180))
    col = (130, 60, 180, alpha)
    gd.ellipse([CX-r, CY-r, CX+r, CY+r], fill=col)
img = Image.alpha_composite(img, glow)

# ── light vignette (top corners darker) ───────────────────────────────────────
vig = Image.new("RGBA", (W, H), (0,0,0,0))
vd = ImageDraw.Draw(vig)
for r in range(350, 0, -5):
    alpha = int(30 * (1 - r/350))
    vd.ellipse([W//2-r, -100-r//2, W//2+r, H//2+r], fill=(0,0,0,0))
# corner darken
for x in range(0, 200):
    t = (200-x)/200
    a = int(35 * t * t)
    vd.line([(x, 0),(x, 80)], fill=(20, 5, 40, a))
for x in range(W-200, W):
    t = (x-(W-200))/200
    a = int(35 * t * t)
    vd.line([(x, 0),(x, 80)], fill=(20, 5, 40, a))
img = Image.alpha_composite(img, vig)

# ═══════════════════════════════════════════════════════════════════════════════
# 9. SAVE
# ═══════════════════════════════════════════════════════════════════════════════
out = img.convert("RGB")
out.save("/Users/Noel/Documents/Gelou acai/hero-banner.png", "PNG", dpi=(144, 144))
print("Saved: /Users/Noel/Documents/Gelou acai/hero-banner.png")
print(f"Size: {out.size}")
