#!/usr/bin/env python3
"""Texture khoi v3 (16x16, nhieu cai co hoat anh) cho Void Realm.  Chay SAU gen_art.py:  python3 tools/gen_blocks.py"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image  # noqa: E402
from gen_art import hash2, ramp  # noqa: E402


def vnoise(x, y, scale, seed):
    """Value noise TUAN HOAN chu ky 16 -> moi texture ghep lien mach voi khoi canh ben."""
    P = max(1, round(16 / scale))
    gx, gy = (x % 16) * P / 16.0, (y % 16) * P / 16.0
    x0, y0 = int(math.floor(gx)), int(math.floor(gy))
    fx, fy = gx - x0, gy - y0
    sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = hash2(x0 % P, y0 % P, seed)
    b = hash2((x0 + 1) % P, y0 % P, seed)
    c = hash2(x0 % P, (y0 + 1) % P, seed)
    d = hash2((x0 + 1) % P, (y0 + 1) % P, seed)
    return (a + (b - a) * sx) * (1 - sy) + (c + (d - c) * sx) * sy

BLOCK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources", "assets", "voidrealm", "textures", "block")

ST = [(8, 4, 20), (20, 12, 46), (38, 24, 82), (62, 44, 128), (98, 74, 176)]
VIOL = [(30, 14, 90), (80, 40, 190), (150, 100, 245), (225, 200, 255)]
CYAN = [(10, 70, 100), (30, 170, 200), (110, 240, 245), (240, 255, 255)]
GOLD = [(90, 54, 12), (170, 112, 26), (238, 186, 66), (255, 238, 160)]
PINK = [(110, 20, 110), (200, 60, 200), (250, 130, 250), (255, 225, 255)]
STEEL = [(18, 14, 40), (50, 40, 96), (98, 84, 168), (170, 156, 238)]
SOIL = [(14, 8, 22), (30, 16, 44), (54, 30, 70), (84, 52, 104)]


def save(name, frames, frametime=4, interpolate=True):
    """frames: danh sach Image 16x16. 1 khung -> anh tinh (xoa mcmeta cu)."""
    path = os.path.join(BLOCK, name + ".png")
    meta = path + ".mcmeta"
    if len(frames) == 1:
        frames[0].save(path)
        if os.path.exists(meta):
            os.remove(meta)
        return
    sheet = Image.new("RGBA", (16, 16 * len(frames)), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        sheet.paste(fr, (0, 16 * i))
    sheet.save(path)
    with open(meta, "w") as fp:
        json.dump({"animation": {"frametime": frametime, "interpolate": interpolate}}, fp)


def new():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 255))


def px(im, x, y, c, a=255):
    im.putpixel((x % 16, y % 16), (c[0], c[1], c[2], a))


def stone_cell(x, y, seed, scale=3.0, bias=0.0, cols=ST):
    n = 0.55 * vnoise(x, y, scale, seed) + 0.3 * vnoise(x, y, scale * 0.5, seed + 7) + 0.15 * hash2(x, y, seed + 3)
    return ramp(cols, max(0.0, min(1.0, 0.18 + n * 0.62 + bias)))


# ------------------------------------------------------------------ void_stone (anim)
def void_stone():
    N = 8
    frames = []
    for f in range(N):
        im = new()
        for y in range(16):
            for x in range(16):
                c = stone_cell(x, y, 11)
                r1 = abs(2 * vnoise(x, y, 4.0, 21) - 1)
                r2 = abs(2 * vnoise(x, y, 5.0, 33) - 1)
                crack = min(r1, r2)
                if crack < 0.075:
                    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * (f / N + hash2(x // 3, y // 3, 5)))
                    c = ramp(VIOL, 0.25 + 0.5 * pulse)
                elif crack < 0.13:
                    c = ramp(ST, 0.1 + 0.2 * hash2(x, y, 9))
                px(im, x, y, c)
        for k in range(3):
            sx, sy = int(hash2(k, 1, 40) * 16), int(hash2(k, 2, 41) * 16)
            tw = 0.5 + 0.5 * math.sin(2 * math.pi * (f / N + k * 0.31))
            if tw > 0.7:
                px(im, sx, sy, (235, 225, 255))
        frames.append(im)
    save("void_stone", frames, 6)


# ------------------------------------------------------------------ void_bricks
def void_bricks():
    im = new()
    for y in range(16):
        row = y // 4
        off = 0 if row % 2 == 0 else 4
        for x in range(16):
            bx = ((x + off) % 8)
            brick = (x + off) // 8
            seedn = row * 7 + brick * 13
            tone = 0.42 + 0.22 * hash2(row, brick, 61)
            n = vnoise(x, y, 2.2, 17) - 0.5
            t = tone + n * 0.3
            ly = y % 4
            if bx == 0 or ly == 3:      # vua
                c = ramp(ST, 0.05 + 0.1 * hash2(x, y, 3))
                if bx == 0 and ly != 3 and hash2(x, y, 77) > 0.8:
                    c = ramp(VIOL, 0.3)
            else:
                if ly == 0 or bx == 1:
                    t += 0.2
                if ly == 2 or bx == 7:
                    t -= 0.14
                c = ramp(ST, max(0.0, min(1.0, t)))
            px(im, x, y, c)
    # ruột sang: vai vien ky tu cyan nho
    for (x, y) in ((3, 1), (11, 5), (6, 9), (14, 13)):
        px(im, x, y, CYAN[2])
        px(im, x + 1, y, CYAN[1])
    save("void_bricks", [im])


# ------------------------------------------------------------------ void_tile
def void_tile():
    im = new()
    for y in range(16):
        for x in range(16):
            tx, ty = x % 8, y % 8
            d = (tx + ty) / 14.0
            t = 0.55 - 0.25 * d + (vnoise(x, y, 2.0, 5) - 0.5) * 0.18
            if tx in (0, 7) or ty in (0, 7):
                c = ramp(ST, 0.08)
                if tx in (0, 7) and ty in (0, 7):
                    c = GOLD[2]
            elif tx in (1,) or ty in (1,):
                c = ramp(ST, t + 0.2)
            else:
                c = ramp(ST, t)
            # lang khung vang mong sat vien
            if (tx in (1, 6) and 1 <= ty <= 6) or (ty in (1, 6) and 1 <= tx <= 6):
                c = ramp(GOLD, 0.35 + 0.15 * hash2(x, y, 2)) if hash2(x, y, 90) > 0.35 else c
            px(im, x, y, c)
        # kim cuong giua o tile
    for cx, cy in ((3, 3), (11, 3), (3, 11), (11, 11)):
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            px(im, cx + dx, cy + dy, CYAN[2] if (dx + dy) % 2 == 0 else CYAN[1])
    save("void_tile", [im])


# ------------------------------------------------------------------ void_pillar
def void_pillar():
    side = new()
    top = new()
    for y in range(16):
        for x in range(16):
            col = x % 4
            t = [0.42, 0.62, 0.72, 0.5][col] + (vnoise(x, y, 3.0, 8) - 0.5) * 0.2
            c = ramp(ST, t)
            if col == 3:
                c = ramp(ST, 0.1)
            if y <= 1 or y >= 14:
                c = ramp(GOLD, 0.45 + 0.35 * (1 if y in (0, 15) else 0)) if y in (0, 1, 14, 15) else c
                if y in (1, 14):
                    c = ramp(GOLD, 0.25)
            elif y in (2, 13):
                c = ramp(ST, 0.06)
            px(side, x, y, c)
    for y in range(16):
        for x in range(16):
            d = max(abs(x - 7.5), abs(y - 7.5))
            r = math.hypot(x - 7.5, y - 7.5)
            if d > 7:
                c = ramp(GOLD, 0.4 + 0.2 * hash2(x, y, 3))
            elif d > 6:
                c = ramp(ST, 0.08)
            elif r > 5.2:
                c = ramp(ST, 0.45 + (vnoise(x, y, 2.5, 9) - 0.5) * 0.3)
            elif r > 4.2:
                c = ramp(VIOL, 0.45 + 0.2 * math.sin(math.atan2(y - 7.5, x - 7.5) * 4))
            elif r > 2.6:
                c = ramp(ST, 0.3)
            else:
                c = ramp(CYAN, 0.45 + 0.4 * (1 - r / 2.6))
            px(top, x, y, c)
    save("void_pillar", [side])
    save("void_pillar_top", [top])


# ------------------------------------------------------------------ void_chiseled (anim)
def void_chiseled():
    frames = []
    N = 8
    for f in range(N):
        im = new()
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * f / N)
        for y in range(16):
            for x in range(16):
                d = max(abs(x - 7.5), abs(y - 7.5))
                c = ramp(ST, 0.42 + (vnoise(x, y, 2.5, 4) - 0.5) * 0.25)
                if d > 6.8:
                    c = ramp(GOLD, 0.45 + 0.15 * hash2(x, y, 6))
                elif d > 5.8:
                    c = ramp(ST, 0.06)
                diamond = abs(x - 7.5) + abs(y - 7.5)
                if diamond < 6.2 and d <= 5.8:
                    if diamond > 5.0:
                        c = ramp(VIOL, 0.35 + 0.35 * pulse)
                    elif diamond > 2.6:
                        c = ramp(ST, 0.2)
                    elif diamond > 1.2:
                        c = ramp(CYAN, 0.4 + 0.5 * pulse)
                    else:
                        c = (10, 6, 30)
                px(im, x, y, c)
        px(im, 7, 7, (6, 2, 18))
        px(im, 8, 8, (6, 2, 18))
        px(im, 8, 7, (240, 255, 255) if pulse > 0.4 else CYAN[2])
        frames.append(im)
    save("void_chiseled", frames, 5)


# ------------------------------------------------------------------ void_soil
def void_soil():
    top, side, bot = new(), new(), new()
    for y in range(16):
        for x in range(16):
            c = ramp(SOIL, 0.25 + 0.55 * (0.6 * vnoise(x, y, 2.4, 5) + 0.4 * hash2(x, y, 6)))
            px(bot, x, y, c)
            moss = vnoise(x, y, 3.2, 14)
            t = ramp(SOIL, 0.3 + 0.5 * (0.5 * vnoise(x, y, 2.0, 7) + 0.5 * hash2(x, y, 8)))
            if moss > 0.48:
                t = ramp(CYAN, 0.12 + 0.3 * hash2(x, y, 20))
                if hash2(x, y, 22) > 0.86:
                    t = ramp(CYAN, 0.8)
            elif moss > 0.4:
                t = ramp(VIOL, 0.12 + 0.2 * hash2(x, y, 23))
            px(top, x, y, t)
            fringe = 3 + int(hash2(x, 0, 31) * 3)
            if y < fringe:
                s = ramp(CYAN, 0.1 + 0.28 * hash2(x, y, 40)) if hash2(x, y, 41) > 0.2 else ramp(VIOL, 0.3)
                if y == fringe - 1 and hash2(x, y, 42) > 0.6:
                    s = ramp(CYAN, 0.8)
            else:
                s = c
            px(side, x, y, s)
    save("void_soil_top", [top])
    save("void_soil_side", [side])
    save("void_soil", [bot])


# ------------------------------------------------------------------ void_crystal_block (anim)
def void_crystal_block():
    rnd = random.Random(3)
    pts = [(rnd.random() * 16, rnd.random() * 16) for _ in range(9)]
    shade = [rnd.uniform(0.3, 0.85) for _ in pts]
    N = 8
    frames = []
    for f in range(N):
        im = new()
        for y in range(16):
            for x in range(16):
                best, bd, second = 0, 99, 99
                for i, (px_, py_) in enumerate(pts):
                    dx = min(abs(x - px_), 16 - abs(x - px_))
                    dy = min(abs(y - py_), 16 - abs(y - py_))
                    d = math.hypot(dx, dy)
                    if d < bd:
                        second, bd, best = bd, d, i
                    elif d < second:
                        second = d
                t = shade[best]
                sweep = (x + y - f * 4) % 16
                if sweep < 3:
                    t += 0.22 - 0.06 * sweep
                c = ramp(VIOL, min(1.0, t))
                if second - bd < 0.9:
                    c = ramp(VIOL, 0.12 + 0.15 * hash2(x, y, 3))
                px(im, x, y, c)
        frames.append(im)
    save("void_crystal_block", frames, 3)


# ------------------------------------------------------------------ void_steel_block
def void_steel_block():
    im = new()
    for y in range(16):
        for x in range(16):
            tx, ty = x % 8, y % 8
            t = 0.5 + (vnoise(x, y, 2.5, 3) - 0.5) * 0.2 + (0.12 if (tx + ty) in (8, 9) else 0.0) - 0.04 * abs(tx - 3.5)
            c = ramp(STEEL, t)
            if tx in (0, 7) or ty in (0, 7):
                c = ramp(STEEL, 0.05) if (tx in (0,) or ty in (0,)) else ramp(STEEL, 0.9)
            if tx in (1, 6) and ty in (1, 6):
                c = GOLD[2]
            px(im, x, y, c)
    for (x, y) in ((4, 4), (12, 4), (4, 12), (12, 12)):
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            px(im, x - 1 + dx, y - 1 + dy, ramp(CYAN, 0.45 + 0.25 * ((dx + dy) % 2)))
    save("void_steel_block", [im])


# ------------------------------------------------------------------ ore
def ore(name, base_bias, deep):
    N = 8
    frames = []
    clusters = [(3, 3, 0.0), (11, 4, 0.33), (6, 11, 0.66), (13, 12, 0.5)]
    for f in range(N):
        im = new()
        for y in range(16):
            for x in range(16):
                c = stone_cell(x, y, 51 if deep else 11, bias=base_bias, cols=[(6, 4, 14), (14, 10, 30), (26, 18, 56), (44, 32, 92), (70, 54, 132)] if deep else ST)
                px(im, x, y, c)
        for (cx, cy, ph) in clusters:
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * (f / N + ph))
            for dx, dy, shade in ((0, 0, 0.85), (1, 0, 0.6), (0, 1, 0.7), (1, 1, 0.45), (-1, 1, 0.4), (0, 2, 0.35), (1, 2, 0.5), (2, 1, 0.3), (0, -1, 0.5)):
                s = shade * (0.75 + 0.25 * pulse)
                px(im, cx + dx, cy + dy, ramp(VIOL, s))
            px(im, cx, cy, ramp(VIOL, 0.7 + 0.3 * pulse))
            if pulse > 0.75:
                px(im, cx - 1, cy - 1, (240, 230, 255))
            for dx, dy in ((-2, 0), (3, 1), (0, 3), (-1, -1)):
                p = (cx + dx, cy + dy)
                r, g, b, a = im.getpixel((p[0] % 16, p[1] % 16))
                px(im, p[0], p[1], (min(255, r + int(30 * pulse)), min(255, g + int(12 * pulse)), min(255, b + int(45 * pulse))))
        frames.append(im)
    save(name, frames, 5)


# ------------------------------------------------------------------ khung cong + mat cong
def portal_frame():
    for lit in (False, True):
        N = 8 if lit else 1
        frames = []
        for f in range(N):
            im = new()
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * f / 8)
            for y in range(16):
                for x in range(16):
                    d = max(abs(x - 7.5), abs(y - 7.5))
                    c = ramp(ST, 0.34 + (vnoise(x, y, 2.5, 12) - 0.5) * 0.25)
                    if d > 6.9:
                        c = ramp(GOLD, 0.4 + 0.2 * hash2(x, y, 6))
                    elif d > 5.9:
                        c = ramp(ST, 0.05)
                    px(im, x, y, c)
            # ky tu: duong doc + vong + nhanh
            glow = ramp(CYAN, 0.55 + 0.4 * pulse) if lit else ramp(ST, 0.5)
            glow2 = ramp(CYAN, 0.9) if lit else ramp(ST, 0.62)
            for y in range(3, 13):
                px(im, 7, y, glow)
                px(im, 8, y, glow)
            for (x, y) in ((5, 5), (10, 5), (5, 10), (10, 10), (4, 7), (11, 8), (6, 4), (9, 11)):
                px(im, x, y, glow)
            for (x, y) in ((7, 7), (8, 8), (7, 8), (8, 7)):
                px(im, x, y, glow2)
            frames.append(im)
        save("void_portal_frame_lit" if lit else "void_portal_frame", frames, 5)


def void_portal():
    N = 32
    frames = []
    for f in range(N):
        t = f / N
        im = Image.new("RGBA", (16, 16))
        for y in range(16):
            for x in range(16):
                a = math.sin(2 * math.pi * (x / 16 * 2 + t))
                b = math.sin(2 * math.pi * (y / 16 * 3 - t))
                c2 = math.sin(2 * math.pi * ((x + y) / 16 + 2 * t))
                d = math.sin(2 * math.pi * ((x - 2 * y) / 16 - t))
                v = (a + b + c2 + d) / 4.0 * 0.5 + 0.5
                col = ramp([(26, 8, 80), (80, 36, 190), (60, 160, 230), (170, 240, 255)], min(1.0, v * 1.05))
                alpha = int(150 + 90 * v)
                im.putpixel((x, y), (col[0], col[1], col[2], alpha))
        for k in range(4):
            sx, sy = int(hash2(k, 5, 60) * 16), int(hash2(k, 6, 61) * 16)
            if math.sin(2 * math.pi * (t + k * 0.25)) > 0.8:
                im.putpixel((sx, sy), (255, 255, 255, 255))
        frames.append(im)
    save("void_portal", frames, 2)


# ------------------------------------------------------------------ ban te
def altar():
    side, top = new(), new()
    inner, inner_on = [], []
    for y in range(16):
        for x in range(16):
            c = ramp(ST, 0.4 + (vnoise(x, y, 2.5, 5) - 0.5) * 0.3 + (0.15 if x % 8 in (1,) else 0))
            if y in (0, 15):
                c = ramp(GOLD, 0.5)
            elif y in (1, 14):
                c = ramp(ST, 0.05)
            if (x, y) in ((7, 7), (8, 8), (7, 8), (8, 7)):
                c = CYAN[2]
            px(side, x, y, c)
            d = max(abs(x - 7.5), abs(y - 7.5))
            c2 = ramp(ST, 0.45 + (vnoise(x, y, 2.5, 8) - 0.5) * 0.25)
            if d > 6.5:
                c2 = ramp(GOLD, 0.5)
            elif d > 5.5:
                c2 = ramp(ST, 0.06)
            px(top, x, y, c2)
    save("void_altar_side", [side])
    save("void_altar_top", [top])
    for on in (False, True):
        frames = []
        for f in range(8):
            im = new()
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * f / 8)
            for y in range(16):
                for x in range(16):
                    r = math.hypot(x - 7.5, y - 7.5)
                    ang = math.atan2(y - 7.5, x - 7.5)
                    c = ramp(ST, 0.12)
                    ring = abs(r - 5.5)
                    if ring < 0.8:
                        c = ramp(CYAN if on else VIOL, (0.5 + 0.45 * pulse) if on else 0.4)
                    spokes = abs(math.sin(ang * 4 + (f * 0.4 if on else 0)))
                    if r < 4.6 and r > 1.5 and spokes < 0.18:
                        c = ramp(CYAN if on else VIOL, 0.6 + 0.3 * pulse)
                    if r <= 1.5:
                        c = ramp(CYAN, 0.8 + 0.2 * pulse) if on else ramp(VIOL, 0.5)
                    px(im, x, y, c)
            frames.append(im)
        save("void_altar_inner_on" if on else "void_altar_inner", frames, 5)


if __name__ == "__main__":
    void_stone()
    void_bricks()
    void_tile()
    void_pillar()
    void_chiseled()
    void_soil()
    void_crystal_block()
    void_steel_block()
    ore("void_crystal_ore", 0.0, False)
    ore("deepslate_void_crystal_ore", -0.05, True)
    portal_frame()
    void_portal()
    altar()
    print("texture khoi v3 xong")
