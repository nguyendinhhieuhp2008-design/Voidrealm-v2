#!/usr/bin/env python3
"""Sinh toan bo texture (PNG) cho mod Void Realm bang Pillow.

Chay:  python3 tools/gen_textures.py
Texture cua vat pham/khoi la 16x16, texture quai/giap theo dung layout cua model vanilla.
Ban co the sua mau/hinh o day roi chay lai, hoac thay truc tiep file PNG trong
src/main/resources/assets/voidrealm/textures.
"""
import os
import random
from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources", "assets", "voidrealm", "textures")
ITEM_DIR = os.path.join(ROOT, "item")
BLOCK_DIR = os.path.join(ROOT, "block")
ENTITY_DIR = os.path.join(ROOT, "entity")
ARMOR_DIR = os.path.join(ROOT, "models", "armor")
for d in (ITEM_DIR, BLOCK_DIR, ENTITY_DIR, ARMOR_DIR):
    os.makedirs(d, exist_ok=True)

TRANSPARENT = (0, 0, 0, 0)


# ------------------------------------------------------------------ mau sac
def clamp(v):
    return max(0, min(255, int(v)))


def shade(c, f):
    return (clamp(c[0] * f), clamp(c[1] * f), clamp(c[2] * f), 255)


def mix(a, b, t):
    return (clamp(a[0] + (b[0] - a[0]) * t), clamp(a[1] + (b[1] - a[1]) * t), clamp(a[2] + (b[2] - a[2]) * t), 255)


VOID_BASE = (92, 62, 150)
VOID_LIGHT = (160, 120, 225)
VOID_DARK = (44, 28, 84)
OUTLINE = (18, 10, 34, 255)
STICK = (122, 88, 52)
STICK_DARK = (80, 56, 32)
CYAN = (127, 224, 255)
MAGENTA = (255, 92, 225)
ORANGE = (255, 138, 61)
GOLD = (236, 196, 72)


class Canvas:
    def __init__(self, w=16, h=16):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w, h), TRANSPARENT)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            if len(c) == 3:
                c = (c[0], c[1], c[2], 255)
            self.img.putpixel((x, y), c)

    def get(self, x, y):
        return self.img.getpixel((x, y))

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def circle(self, cx, cy, r, c_fn):
        for y in range(self.h):
            for x in range(self.w):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if d <= r:
                    self.px(x, y, c_fn(x, y, d))

    def outline(self, color=OUTLINE):
        src = self.img.copy()
        for y in range(self.h):
            for x in range(self.w):
                if src.getpixel((x, y))[3] == 0:
                    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                        if 0 <= nx < self.w and 0 <= ny < self.h and src.getpixel((nx, ny))[3] > 0:
                            self.img.putpixel((x, y), color)
                            break

    def save(self, path):
        self.img.save(path)


# ------------------------------------------------------------------ hinh dang tai su dung
def stick(c, x0, y0, x1, y1):
    c.line(x0, y0, x1, y1, shade(STICK, 1.0))
    c.line(x0 + 1, y0, x1 + 1, y1, shade(STICK_DARK, 1.0)) if False else None


def blade(c, x0, y0, length, base, light, dark):
    """Luoi di cheo huong len-phai, rong ~2px."""
    for i in range(length + 1):
        x, y = x0 + i, y0 - i
        c.px(x, y, light)
        c.px(x + 1, y, base)
        c.px(x, y + 1, base)
        c.px(x + 1, y + 1, dark)


def tool_handle(c, x0=2, y0=13, x1=9, y1=6):
    c.line(x0, y0, x1, y1, shade(STICK, 1.0))
    c.line(x0 - 1, y0 + 1, x0, y0, shade(STICK_DARK, 1.0))


def draw_sword(base, light, dark, guard, accent=None, crack=None):
    c = Canvas()
    blade(c, 5, 10, 7, base, light, dark)
    c.px(13, 2, light)
    if accent and crack:
        for i, (x, y) in enumerate([(7, 8), (9, 6), (11, 4)]):
            c.px(x, y, crack)
    # chan kiem
    c.line(3, 9, 6, 12, guard)
    c.line(4, 9, 6, 11, shade(guard, 0.75)) if False else None
    # tay cam
    c.line(2, 13, 4, 11, shade(STICK, 1.0))
    c.px(1, 14, shade(STICK_DARK, 1.0))
    c.outline()
    return c


def draw_pickaxe(base, light, dark):
    c = Canvas()
    tool_handle(c, 2, 14, 11, 5)
    pts = [(4, 5), (5, 3), (7, 2), (10, 2), (12, 3), (13, 5), (13, 8), (12, 10)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], base)
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1] + 1, b[0] - 1, b[1] + 1, dark) if False else None
    for x, y in [(5, 3), (7, 2), (10, 2)]:
        c.px(x, y, light)
    for x, y in [(13, 6), (13, 7), (12, 9)]:
        c.px(x, y, dark)
    c.px(11, 5, shade(STICK, 1.0))
    c.outline()
    return c


def draw_axe(base, light, dark):
    c = Canvas()
    tool_handle(c, 2, 14, 10, 6)
    for y, (x0, x1) in zip(range(2, 10), [(8, 12), (7, 13), (7, 13), (8, 13), (9, 13), (9, 12), (9, 11), (9, 10)]):
        for x in range(x0, x1 + 1):
            c.px(x, y, base)
    for y in range(2, 10):
        for x in range(6, 14):
            p = c.get(x, y)
            if p[3] > 0:
                if x == min(xx for xx in range(16) if c.get(xx, y)[3] > 0):
                    c.px(x, y, light)
                elif y >= 7 and x == max(xx for xx in range(16) if c.get(xx, y)[3] > 0):
                    c.px(x, y, dark)
    c.outline()
    return c


def draw_shovel(base, light, dark):
    c = Canvas()
    tool_handle(c, 2, 14, 10, 6)
    c.circle(11.5, 3.5, 3.2, lambda x, y, d: light if (x + y) < 14 else (dark if d > 2.4 else base))
    c.px(10, 6, shade(STICK, 1.0))
    c.outline()
    return c


def draw_hoe(base, light, dark):
    c = Canvas()
    tool_handle(c, 2, 14, 10, 6)
    c.rect(7, 2, 13, 3, base)
    c.rect(7, 2, 13, 2, light)
    c.rect(11, 4, 13, 5, base)
    c.rect(13, 4, 13, 5, dark)
    c.outline()
    return c


def draw_scythe(base, light, dark, accent):
    c = Canvas()
    c.line(3, 14, 11, 3, shade(STICK, 0.9))
    c.line(4, 14, 12, 3, shade(STICK_DARK, 1.0))
    pts = [(10, 2), (8, 1), (5, 1), (3, 3), (2, 6)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], base)
        c.line(a[0], a[1] + 1, b[0], b[1] + 1, dark)
    c.px(5, 1, light)
    c.px(8, 1, light)
    c.px(3, 3, accent)
    c.px(2, 6, accent)
    c.px(12, 2, accent)
    c.outline()
    return c


def draw_spear(base, light, dark, accent):
    c = Canvas()
    c.line(2, 14, 11, 5, shade(STICK, 1.0))
    c.line(1, 14, 10, 5, shade(STICK_DARK, 1.0)) if False else None
    # dau giao hinh la
    for i, (x, y) in enumerate([(11, 5), (12, 4), (13, 3), (14, 2)]):
        c.px(x, y, base)
        c.px(x - 1, y, light)
        c.px(x, y + 1, dark)
    c.px(12, 3, base)
    c.px(13, 2, light)
    c.px(12, 5, accent)
    c.px(10, 5, accent)
    c.px(11, 4, accent)
    c.px(11, 6, accent)
    c.outline()
    return c


def draw_staff(accent):
    c = Canvas()
    c.line(3, 14, 10, 7, shade(STICK, 1.0))
    c.line(4, 14, 11, 7, shade(STICK_DARK, 1.0)) if False else None
    # vong kim loai
    for x, y in [(10, 6), (11, 5)]:
        c.px(x, y, shade(VOID_BASE, 1.0))
    # vien ngoc hut
    c.circle(12, 4, 2.9, lambda x, y, d: mix((20, 8, 40), accent, max(0.0, 1.0 - d / 3.0)))
    c.px(11, 3, (255, 255, 255))
    for x, y in [(9, 2), (14, 7), (14, 1), (9, 7)]:
        c.px(x, y, shade(accent, 0.8))
    c.outline()
    return c


def draw_ingot(base, light, dark):
    c = Canvas()
    for y, (x0, x1) in zip(range(5, 12), [(5, 12), (4, 12), (3, 11), (3, 11), (3, 10), (4, 10), (5, 10)]):
        for x in range(x0, x1 + 1):
            c.px(x, y, base)
    for x in range(5, 13):
        c.px(x, 5, light)
    for x in range(3, 12):
        c.px(x, 8, shade(base, 1.08))
    for y in range(9, 12):
        for x in range(3, 11):
            if c.get(x, y)[3] > 0:
                c.px(x, y, dark if y == 11 or x == 10 else base)
    c.px(6, 6, (255, 255, 255))
    c.outline()
    return c


def draw_shard():
    c = Canvas()
    pts = [(8, 1), (12, 6), (10, 14), (6, 14), (4, 6)]
    from PIL import ImageDraw
    d = ImageDraw.Draw(c.img)
    d.polygon(pts, fill=(112, 70, 200, 255))
    d.polygon([(8, 1), (4, 6), (7, 8), (8, 4)], fill=(176, 140, 255, 255))
    d.polygon([(8, 1), (12, 6), (10, 8), (8, 4)], fill=(140, 96, 235, 255))
    d.polygon([(7, 8), (10, 8), (10, 14), (6, 14)], fill=(80, 46, 150, 255))
    c.px(8, 3, (255, 255, 255))
    c.px(7, 5, CYAN + (255,))
    c.px(9, 10, CYAN + (255,))
    c.outline()
    return c


def draw_silk():
    c = Canvas()
    pts = [(3, 12), (4, 9), (6, 7), (9, 7), (11, 9), (11, 11), (9, 12), (7, 11), (7, 9), (9, 9)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], (236, 176, 255, 255))
    for x, y in [(4, 9), (9, 7), (11, 10)]:
        c.px(x, y, (255, 255, 255, 255))
    c.line(11, 11, 13, 13, (200, 120, 240, 255))
    c.px(13, 14, MAGENTA + (255,))
    c.outline()
    return c


def draw_core():
    c = Canvas()
    c.circle(7.5, 7.5, 6.2, lambda x, y, d: mix((18, 6, 36), MAGENTA, max(0.0, (d - 2.0) / 4.5)) if d < 5.2 else (54, 20, 90, 255))
    c.circle(7.5, 7.5, 2.2, lambda x, y, d: mix((255, 255, 255), CYAN, d / 2.2))
    for x, y in [(3, 3), (12, 4), (4, 12), (12, 12)]:
        c.px(x, y, (255, 200, 250, 255))
    c.outline()
    return c


def draw_apple():
    c = Canvas()
    c.circle(7.5, 9, 5.2, lambda x, y, d: mix((90, 40, 160), (30, 10, 60), min(1.0, d / 5.2)))
    c.circle(5.5, 7, 1.4, lambda x, y, d: mix((220, 200, 255), (140, 100, 220), d / 1.4))
    c.line(8, 4, 9, 1, shade(STICK, 1.0))
    c.px(10, 2, CYAN + (255,))
    c.px(11, 3, CYAN + (255,))
    c.px(10, 3, (80, 200, 230, 255))
    c.px(9, 12, MAGENTA + (255,))
    c.outline()
    return c


ARMOR_TEMPLATES = {
    "helmet": [
        "................",
        "................",
        "....oooooooo....",
        "...obbbbbbbbo...",
        "..oblllbbbbbbo..",
        "..oblbbbbbbbdo..",
        "..obbbbbbbbbdo..",
        "..obbbbbbbbbdo..",
        "..obaaaaaaaabdo.",
        "..obbbbbbbbbdo..",
        "..obbo....obbdo.",
        "..obbo....obbdo.",
        "..oooo....oooo..",
        "................",
        "................",
        "................",
    ],
    "chestplate": [
        "................",
        "..ooo......ooo..",
        ".obbbo....obbbo.",
        ".oblbbooooobbbdo",
        ".obbbbbbbbbbbbdo",
        ".obbbbbbbbbbbbdo",
        "..obbbbaaabbbdo.",
        "..obbbbaaabbbdo.",
        "..obbbbbabbbbdo.",
        "..obbbbbbbbbbdo.",
        "..obbbbbbbbbbdo.",
        "..obbbbbbbbbbdo.",
        "..obbbbbbbbbbdo.",
        "...oooooooooooo.",
        "................",
        "................",
    ],
    "leggings": [
        "................",
        "..oooooooooooo..",
        "..obbbbbbbbbbo..",
        "..oblaaaaaaabdo.",
        "..obbbbbbbbbbdo.",
        "..obbbbbbbbbbdo.",
        "..obbbooooobbdo.",
        "..obbbo...obbdo.",
        "..obbbo...obbdo.",
        "..obbbo...obbdo.",
        "..obbbo...obbdo.",
        "..obbbo...obbdo.",
        "..oooo....oooo..",
        "................",
        "................",
        "................",
    ],
    "boots": [
        "................",
        "................",
        "................",
        "................",
        "..oooo....oooo..",
        "..obbbo..obbbdo.",
        "..obbbo..obbbdo.",
        "..obbbo..obbbdo.",
        "..obbbo..obbbdo.",
        ".obbbbbo.obbbbdo",
        ".oblbbbo.oblbbdo",
        ".oaaaaao.oaaaaao",
        ".ooooooo.ooooooo",
        "................",
        "................",
        "................",
    ],
}


def draw_armor_icon(kind, base, light, dark, accent):
    rows = ARMOR_TEMPLATES[kind]
    assert len(rows) == 16, kind
    c = Canvas()
    cmap = {"o": OUTLINE, "b": shade(base, 1.0), "l": shade(light, 1.0), "d": shade(dark, 1.0), "a": shade(accent, 1.0)}
    for y, row in enumerate(rows):
        assert len(row) == 16, (kind, y, len(row))
        for x, ch in enumerate(row):
            if ch in cmap:
                c.px(x, y, cmap[ch])
    return c


# ------------------------------------------------------------------ vat pham
def make_items():
    steel = (VOID_BASE, VOID_LIGHT, VOID_DARK)
    draw_ingot(*steel).save(os.path.join(ITEM_DIR, "void_steel_ingot.png"))
    draw_shard().save(os.path.join(ITEM_DIR, "void_shard.png"))
    draw_silk().save(os.path.join(ITEM_DIR, "phase_silk.png"))
    draw_core().save(os.path.join(ITEM_DIR, "rift_core.png"))
    draw_apple().save(os.path.join(ITEM_DIR, "void_apple.png"))

    draw_sword(*steel, guard=shade(VOID_DARK, 1.2)).save(os.path.join(ITEM_DIR, "void_steel_sword.png"))
    draw_pickaxe(*steel).save(os.path.join(ITEM_DIR, "void_steel_pickaxe.png"))
    draw_axe(*steel).save(os.path.join(ITEM_DIR, "void_steel_axe.png"))
    draw_shovel(*steel).save(os.path.join(ITEM_DIR, "void_steel_shovel.png"))
    draw_hoe(*steel).save(os.path.join(ITEM_DIR, "void_steel_hoe.png"))

    draw_sword((60, 20, 110), (255, 140, 240), (28, 6, 52), guard=shade(MAGENTA, 0.8), accent=True, crack=CYAN + (255,)).save(
        os.path.join(ITEM_DIR, "rift_blade.png"))
    draw_scythe((70, 40, 130), (190, 150, 255), (30, 14, 60), accent=(170, 90, 255)).save(os.path.join(ITEM_DIR, "void_reaper.png"))
    draw_spear((150, 110, 230), (225, 205, 255), (70, 40, 130), accent=CYAN).save(os.path.join(ITEM_DIR, "voidpiercer.png"))
    draw_staff(CYAN).save(os.path.join(ITEM_DIR, "gravity_staff.png"))

    sets = {
        "void_steel": ((VOID_BASE, VOID_LIGHT, VOID_DARK, CYAN), ["helmet", "chestplate", "leggings", "boots"],
                       ["void_steel_helmet", "void_steel_chestplate", "void_steel_leggings", "void_steel_boots"]),
        "phase_cloth": (((150, 86, 180), (225, 170, 250), (84, 42, 116), MAGENTA), ["helmet", "chestplate", "leggings", "boots"],
                        ["phase_cloth_hood", "phase_cloth_tunic", "phase_cloth_leggings", "phase_cloth_boots"]),
    }
    for _, (cols, kinds, names) in sets.items():
        for kind, name in zip(kinds, names):
            draw_armor_icon(kind, *cols).save(os.path.join(ITEM_DIR, name + ".png"))


# ------------------------------------------------------------------ khoi
def noise_fill(c, base, amp, rng):
    for y in range(c.h):
        for x in range(c.w):
            f = 1.0 + rng.uniform(-amp, amp)
            c.px(x, y, shade(base, f))


def make_blocks():
    rng = random.Random(11)

    def ore(path, base, spot_a, spot_b):
        c = Canvas()
        noise_fill(c, base, 0.10, rng)
        # cac cum pha le tim
        clusters = [(3, 3), (10, 4), (5, 10), (12, 12), (8, 7)]
        for cx, cy in clusters:
            for dx, dy in [(0, 0), (1, 0), (0, 1), (1, 1), (-1, 0)]:
                if rng.random() < 0.85:
                    col = spot_a if (dx + dy) % 2 == 0 else spot_b
                    c.px(cx + dx, cy + dy, col + (255,))
            c.px(cx, cy, (230, 215, 255, 255))
        c.save(path)

    ore(os.path.join(BLOCK_DIR, "void_crystal_ore.png"), (128, 128, 132), (130, 80, 235), (96, 60, 190))
    ore(os.path.join(BLOCK_DIR, "deepslate_void_crystal_ore.png"), (74, 74, 80), (130, 80, 235), (96, 60, 190))

    # khoi thep hu khong
    c = Canvas()
    for y in range(16):
        for x in range(16):
            f = 1.0 + rng.uniform(-0.05, 0.05)
            col = shade(VOID_BASE, f)
            if x in (0, 15) or y in (0, 15):
                col = shade(VOID_DARK, 1.0)
            elif x in (1, 14) or y in (1, 14):
                col = shade(VOID_LIGHT, 0.9) if (x == 1 or y == 1) else shade(VOID_DARK, 1.3)
            c.px(x, y, col)
    for i in range(3, 13):
        c.px(i, 8, shade(VOID_DARK, 1.2))
        c.px(8, i, shade(VOID_DARK, 1.2))
    for x, y in [(4, 4), (11, 4), (4, 11), (11, 11)]:
        c.px(x, y, CYAN + (255,))
    c.save(os.path.join(BLOCK_DIR, "void_steel_block.png"))

    # da hu khong
    c = Canvas()
    noise_fill(c, (30, 24, 44), 0.18, rng)
    for _ in range(14):
        x, y = rng.randrange(16), rng.randrange(16)
        c.px(x, y, shade((110, 70, 190), rng.uniform(0.6, 1.0)))
    c.save(os.path.join(BLOCK_DIR, "void_stone.png"))

    # gach hu khong
    c = Canvas()
    for y in range(16):
        for x in range(16):
            row = y // 4
            off = 0 if row % 2 == 0 else 4
            mortar = (y % 4 == 3) or ((x + off) % 8 == 7)
            if mortar:
                c.px(x, y, shade((14, 10, 24), 1.0))
            else:
                c.px(x, y, shade((44, 34, 68), 1.0 + rng.uniform(-0.12, 0.12)))
    for _ in range(6):
        x, y = rng.randrange(16), rng.randrange(16)
        if c.get(x, y)[:3] != (14, 10, 24):
            c.px(x, y, shade((120, 80, 200), rng.uniform(0.5, 0.9)))
    c.save(os.path.join(BLOCK_DIR, "void_bricks.png"))

    # den di gioi
    c = Canvas()
    for y in range(16):
        for x in range(16):
            frame = x in (0, 1, 14, 15) or y in (0, 1, 14, 15) or x == y or x + y == 15
            if frame:
                c.px(x, y, shade(VOID_DARK, 1.0 + (0.3 if (x + y) % 2 == 0 else 0.0)))
            else:
                d = ((x - 7.5) ** 2 + (y - 7.5) ** 2) ** 0.5
                c.px(x, y, mix((255, 255, 255), MAGENTA, min(1.0, d / 7.0)))
    c.save(os.path.join(BLOCK_DIR, "rift_lantern.png"))


# ------------------------------------------------------------------ tao hinh theo UV cua model
def faces(u, v, w, h, d):
    """6 mat cua mot hop theo layout texOffs(u,v) cua Minecraft: ten -> (x, y, rong, cao)."""
    return {
        "top": (u + d, v, w, d),
        "bottom": (u + d + w, v, w, d),
        "right": (u, v + d, d, h),
        "front": (u + d, v + d, w, h),
        "left": (u + d + w, v + d, d, h),
        "back": (u + d + w + d, v + d, w, h),
    }


def paint_part(c, u, v, w, h, d, fn):
    for name, (fx, fy, fw, fh) in faces(u, v, w, h, d).items():
        for py in range(fh):
            for px in range(fw):
                col = fn(name, px, py, fw, fh)
                if col is not None:
                    c.px(fx + px, fy + py, col)


def tone(base, rng, amp=0.10):
    return shade(base, 1.0 + rng.uniform(-amp, amp))


def face_shade(name):
    return {"top": 1.15, "bottom": 0.7, "right": 0.9, "front": 1.0, "left": 0.85, "back": 0.8}[name]


# ------------------------------------------------------------------ quai (humanoid 64x64)
def humanoid(path, skin, body, limbs, legs, eye, accent, extra=None, seed=1):
    rng = random.Random(seed)
    c = Canvas(64, 64)

    def head_fn(name, px, py, fw, fh):
        col = tone(skin, rng)
        col = shade(col, face_shade(name))
        if name == "front":
            if py in (3, 4) and px in (1, 2, 5, 6):
                return eye + (255,)
            if py == 6 and 2 <= px <= 5:
                return shade(skin, 0.45)
        return col

    def body_fn(name, px, py, fw, fh):
        col = shade(tone(body, rng), face_shade(name))
        if name == "front" and px in (3, 4) and 2 <= py <= 9:
            return shade(accent, 0.85) + ()
        return col

    def limb_fn(name, px, py, fw, fh):
        col = shade(tone(limbs, rng), face_shade(name))
        if py < 2:
            col = shade(skin, face_shade(name))
        return col

    def leg_fn(name, px, py, fw, fh):
        col = shade(tone(legs, rng), face_shade(name))
        if py >= fh - 2:
            col = shade(col, 0.6)
        return col

    paint_part(c, 0, 0, 8, 8, 8, head_fn)
    paint_part(c, 16, 16, 8, 12, 4, body_fn)
    paint_part(c, 40, 16, 4, 12, 4, limb_fn)
    paint_part(c, 0, 16, 4, 12, 4, leg_fn)
    paint_part(c, 32, 48, 4, 12, 4, limb_fn)
    paint_part(c, 16, 48, 4, 12, 4, leg_fn)
    if extra:
        extra(c, rng)
    c.save(path)


def make_humanoids():
    humanoid(os.path.join(ENTITY_DIR, "void_walker.png"),
             skin=(40, 30, 66), body=(26, 16, 44), limbs=(34, 22, 58), legs=(20, 12, 36),
             eye=CYAN, accent=(120, 80, 220), seed=3)
    humanoid(os.path.join(ENTITY_DIR, "phase_stalker.png"),
             skin=(70, 24, 84), body=(40, 12, 54), limbs=(60, 20, 76), legs=(34, 10, 48),
             eye=(255, 220, 250), accent=MAGENTA, seed=4)

    def brute_extra(c, rng):
        # vet nut cam tren than va mat
        for _ in range(16):
            x, y = rng.randrange(20, 36), rng.randrange(20, 32)
            c.px(x, y, ORANGE + (255,))

    humanoid(os.path.join(ENTITY_DIR, "rift_brute.png"),
             skin=(92, 80, 116), body=(68, 60, 92), limbs=(84, 72, 108), legs=(52, 46, 74),
             eye=ORANGE, accent=ORANGE, extra=brute_extra, seed=5)

    def sovereign_extra(c, rng):
        # mien/vuong mien vang tren dinh dau (mat tren + vien tran)
        fx, fy, fw, fh = faces(0, 0, 8, 8, 8)["top"]
        for x in range(fw):
            for y in range(fh):
                if x in (0, fw - 1) or y in (0, fh - 1):
                    c.px(fx + x, fy + y, GOLD + (255,))
        for name in ("front", "right", "left", "back"):
            fx, fy, fw, fh = faces(0, 0, 8, 8, 8)[name]
            for x in range(fw):
                c.px(fx + x, fy, GOLD + (255,))
        # bieu tuong ngoc o nguc
        fx, fy, fw, fh = faces(16, 16, 8, 12, 4)["front"]
        for dx, dy in [(3, 3), (4, 3), (3, 4), (4, 4)]:
            c.px(fx + dx, fy + dy, MAGENTA + (255,))

    humanoid(os.path.join(ENTITY_DIR, "void_sovereign.png"),
             skin=(22, 14, 36), body=(16, 8, 28), limbs=(20, 12, 34), legs=(12, 6, 22),
             eye=(255, 90, 255), accent=GOLD, extra=sovereign_extra, seed=6)


# ------------------------------------------------------------------ Cung thu (skeleton 64x32)
def make_archer():
    rng = random.Random(8)
    c = Canvas(64, 32)
    bone = (176, 170, 200)

    def head(name, px, py, fw, fh):
        col = shade(tone(bone, rng), face_shade(name))
        if name == "front":
            if py in (3, 4) and px in (1, 2, 5, 6):
                return CYAN + (255,)
        return col

    def torso(name, px, py, fw, fh):
        col = shade(tone((120, 110, 150), rng), face_shade(name))
        if name == "front" and py in (2, 4, 6, 8):
            return shade((60, 50, 90), 1.0)
        return col

    def limb(name, px, py, fw, fh):
        return shade(tone(bone, rng), face_shade(name))

    paint_part(c, 0, 0, 8, 8, 8, head)
    paint_part(c, 16, 16, 8, 12, 4, torso)
    paint_part(c, 40, 16, 2, 12, 2, limb)
    paint_part(c, 0, 16, 2, 12, 2, limb)
    c.save(os.path.join(ENTITY_DIR, "rift_archer.png"))


# ------------------------------------------------------------------ Lon rung (pig 64x32)
def make_boar():
    rng = random.Random(9)
    c = Canvas(64, 32)
    fur = (58, 40, 84)

    # to mau ca ban do cho moi UV deu co mau
    for y in range(32):
        for x in range(64):
            c.px(x, y, shade(fur, 1.0 + rng.uniform(-0.12, 0.12)))

    def head(name, px, py, fw, fh):
        col = shade(tone(fur, rng), face_shade(name))
        if name == "front":
            if py in (3, 4) and px in (1, 2, 5, 6):
                return CYAN + (255,)
            if py == 6 and px in (1, 6):
                return (235, 230, 245, 255)  # ngà
        return col

    def body(name, px, py, fw, fh):
        col = shade(tone(fur, rng), face_shade(name))
        if name in ("top",) and px % 3 == 0:
            return shade((120, 80, 200), 0.8)
        return col

    def snout(name, px, py, fw, fh):
        col = shade(tone((96, 64, 128), rng), face_shade(name))
        if name == "front" and py == 1 and px in (1, 2):
            return (20, 10, 30, 255)
        return col

    def leg(name, px, py, fw, fh):
        col = shade(tone((40, 28, 60), rng), face_shade(name))
        if py >= fh - 1:
            col = shade(col, 0.55)
        return col

    paint_part(c, 0, 0, 8, 8, 8, head)
    paint_part(c, 28, 8, 10, 16, 8, body)
    paint_part(c, 16, 16, 4, 3, 1, snout)
    paint_part(c, 0, 16, 4, 6, 4, leg)
    c.save(os.path.join(ENTITY_DIR, "void_boar.png"))


# ------------------------------------------------------------------ Giap (64x32)
def armor_layers(name, base, light, dark, trim, cloth=False, seed=20):
    rng = random.Random(seed)

    def surface(face, px, py, fw, fh, stripe=True):
        col = shade(tone(base, rng, 0.08), face_shade(face))
        if px == 0 or py == 0:
            col = shade(light, face_shade(face))
        if px == fw - 1 or py == fh - 1:
            col = shade(dark, face_shade(face))
        if cloth and stripe and py % 4 == 2:
            col = shade(trim, 0.7 * face_shade(face) + 0.3)
        if not cloth and stripe and py == 1 and 0 < px < fw - 1:
            col = shade(trim, 0.9)
        return col

    # ---- layer 1: mu + ao + gang tay + giay
    c1 = Canvas(64, 32)

    def helm(face, px, py, fw, fh):
        col = surface(face, px, py, fw, fh)
        if face == "front" and py in (3, 4) and px in (1, 2, 5, 6):
            return shade(trim, 1.0)
        return col

    paint_part(c1, 0, 0, 8, 8, 8, helm)
    paint_part(c1, 16, 16, 8, 12, 4, lambda f, px, py, fw, fh: (
        shade(trim, 1.0) if f == "front" and px in (3, 4) and 3 <= py <= 6 else surface(f, px, py, fw, fh)))
    paint_part(c1, 40, 16, 4, 12, 4, lambda f, px, py, fw, fh: surface(f, px, py, fw, fh, stripe=False))

    def boot(face, px, py, fw, fh):
        if face == "top":
            return None
        if face == "bottom":
            return shade(dark, 0.8)
        if py < fh - 5:
            return None
        return surface(face, px, py, fw, fh, stripe=False)

    paint_part(c1, 0, 16, 4, 12, 4, boot)
    c1.save(os.path.join(ARMOR_DIR, name + "_layer_1.png"))

    # ---- layer 2: quan (than duoi + chan)
    c2 = Canvas(64, 32)

    def belt(face, px, py, fw, fh):
        if face == "top":
            return None
        if py < fh - 4:
            return None
        col = surface(face, px, py, fw, fh, stripe=False)
        if face == "front" and py == fh - 4 and 2 <= px <= 5:
            return shade(trim, 1.0)
        return col

    paint_part(c2, 16, 16, 8, 12, 4, belt)
    paint_part(c2, 0, 16, 4, 12, 4, lambda f, px, py, fw, fh: surface(f, px, py, fw, fh))
    c2.save(os.path.join(ARMOR_DIR, name + "_layer_2.png"))


def make_armor():
    armor_layers("void_steel", VOID_BASE, VOID_LIGHT, VOID_DARK, CYAN, cloth=False, seed=21)
    armor_layers("phase_cloth", (150, 86, 180), (225, 170, 250), (84, 42, 116), MAGENTA, cloth=True, seed=22)


if __name__ == "__main__":
    make_items()
    make_blocks()
    make_humanoids()
    make_archer()
    make_boar()
    make_armor()
    print("Da sinh texture vao", os.path.abspath(ROOT))
