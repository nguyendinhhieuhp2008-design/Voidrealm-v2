#!/usr/bin/env python3
"""Do hoa nang cap cho Void Realm: quai (co lop phat sang *_glow.png), khoi dong (animated),
giap mac tren nguoi va lop 'polish' cho icon vat pham.
Chay: python3 tools/gen_art.py   (tu dong goi gen_textures.py cho icon vat pham truoc)
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_textures as g  # noqa: E402
from PIL import Image  # noqa: E402

ITEM_DIR, BLOCK_DIR, ENTITY_DIR, ARMOR_DIR = g.ITEM_DIR, g.BLOCK_DIR, g.ENTITY_DIR, g.ARMOR_DIR


# ------------------------------------------------------------------ cong cu
def hash2(x, y, seed):
    n = (x * 374761393 + y * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def vnoise(x, y, scale, seed):
    gx, gy = x / scale, y / scale
    x0, y0 = int(math.floor(gx)), int(math.floor(gy))
    fx, fy = gx - x0, gy - y0
    sx, sy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a = hash2(x0, y0, seed)
    b = hash2(x0 + 1, y0, seed)
    c = hash2(x0, y0 + 1, seed)
    d = hash2(x0 + 1, y0 + 1, seed)
    return (a + (b - a) * sx) * (1 - sy) + (c + (d - c) * sx) * sy


def ramp(cols, t):
    t = max(0.0, min(1.0, t)) * (len(cols) - 1)
    i = int(t)
    if i >= len(cols) - 1:
        return tuple(cols[-1]) + (255,)
    f = t - i
    a, b = cols[i], cols[i + 1]
    return tuple(int(a[k] + (b[k] - a[k]) * f) for k in range(3)) + (255,)


def rgba(c, a=255):
    return (c[0], c[1], c[2], a)


FACE_T = {"top": 0.22, "front": 0.0, "right": -0.06, "left": -0.10, "back": -0.14, "bottom": -0.28}


def faces(u, v, w, h, d):
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


class Skin:
    def __init__(self, w, h, seed=1):
        self.w, self.h, self.seed = w, h, seed
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.parts = {}
        self.occ = set()

    def part(self, name, u, v, w, h, d):
        self.parts[name] = (u, v, w, h, d)
        if not hasattr(self, "occ"):
            self.occ = set()
        for yy in range(v, min(self.h, v + d + h)):
            for xx in range(u, min(self.w, u + 2 * d + 2 * w)):
                self.occ.add((xx, yy))

    def alloc(self, name, w, h, d):
        """Tim cho trong tren texture de dat mot hop moi (w x h x d)."""
        rw, rh = 2 * d + 2 * w, d + h
        for v in range(0, self.h - rh + 1):
            for u in range(0, self.w - rw + 1):
                if all((xx, yy) not in self.occ for yy in range(v, v + rh) for xx in range(u, u + rw)):
                    self.part(name, u, v, w, h, d)
                    return u, v
        raise RuntimeError("het cho tren texture cho " + name)

    def glow_part(self, name):
        for face, (fx, fy, fw, fh) in faces(*self.parts[name]).items():
            for yy in range(fy, fy + fh):
                for xx in range(fx, fx + fw):
                    self.glow.putpixel((xx, yy), self.img.getpixel((xx, yy)))

    def rect(self, name, face):
        u, v, w, h, d = self.parts[name]
        return faces(u, v, w, h, d)[face]

    def paint(self, name, cols, base=0.5, contrast=0.38, skip=None):
        """To mau ca 6 mat cua mot hop bang thang mau (co chuyen sac) + nhieu min + toi canh."""
        for face, (fx, fy, fw, fh) in faces(*self.parts[name]).items():
            for py in range(fh):
                for px in range(fw):
                    if skip and skip(face, px, py, fw, fh):
                        continue
                    n = 0.65 * vnoise(fx + px, fy + py, 3.5, self.seed) + 0.35 * hash2(fx + px, fy + py, self.seed + 7)
                    t = base + FACE_T[face] + (n - 0.5) * contrast - 0.12 * py / max(1, fh)
                    if min(px, py, fw - 1 - px, fh - 1 - py) == 0:
                        t -= 0.06
                    self.img.putpixel((fx + px, fy + py), ramp(cols, t))

    def put(self, name, face, x, y, col, glow=False, clear=False):
        fx, fy, fw, fh = self.rect(name, face)
        if 0 <= x < fw and 0 <= y < fh:
            c = (0, 0, 0, 0) if col is None else (rgba(col) if len(col) == 3 else col)
            if clear:
                c = (0, 0, 0, 0)
            self.img.putpixel((fx + x, fy + y), c)
            if glow and not clear:
                self.glow.putpixel((fx + x, fy + y), c)

    def art(self, name, face, rows, legend, ox=0, oy=0):
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch in legend:
                    col, glow = legend[ch]
                    self.put(name, face, x + ox, y + oy, col, glow, clear=(col is None))

    def band(self, name, faces_, y0, y1, cols, base=0.55):
        for face in faces_:
            fx, fy, fw, fh = self.rect(name, face)
            for y in range(y0, min(y1 + 1, fh)):
                for x in range(fw):
                    n = hash2(fx + x, fy + y, self.seed + 3)
                    self.put(name, face, x, y, ramp(cols, base + FACE_T[face] + (n - 0.5) * 0.3 - (y - y0) * 0.05))

    def save(self, base_path, glow=True):
        self.img.save(base_path + ".png")
        if glow:
            self.glow.save(base_path + "_glow.png")


def humanoid_parts(s):
    s.part("head", 0, 0, 8, 8, 8)
    s.part("hat", 32, 0, 8, 8, 8)
    s.part("body", 16, 16, 8, 12, 4)
    s.part("rarm", 40, 16, 4, 12, 4)
    s.part("larm", 32, 48, 4, 12, 4)
    s.part("rleg", 0, 16, 4, 12, 4)
    s.part("lleg", 16, 48, 4, 12, 4)


def both(s, a, b, fn):
    fn(a)
    fn(b)


# ------------------------------------------------------------------ mau chung
CY = (120, 235, 255)
WH = (255, 255, 255)
MG = (255, 90, 235)
VI = (170, 110, 255)
OR = (255, 140, 50)
YE = (255, 210, 90)
GOLD = [(96, 62, 14), (176, 128, 34), (240, 198, 84), (255, 240, 170)]
STONE_M = [(38, 34, 54), (74, 68, 98), (116, 108, 142), (162, 154, 186)]


# ------------------------------------------------------------------ Ke Lang Thang
def void_walker():
    s = Skin(64, 64, 11)
    humanoid_parts(s)
    robe = [(10, 6, 20), (24, 14, 44), (48, 30, 86), (84, 58, 140)]
    skin = [(40, 34, 64), (78, 68, 118), (128, 116, 176), (178, 168, 216)]
    s.paint("head", skin)
    s.paint("body", robe, 0.45)
    for a in ("rarm", "larm"):
        s.paint(a, robe, 0.45)
    for l in ("rleg", "lleg"):
        s.paint(l, robe, 0.35)
    # mui trum: chi phu vien, chua cua so mat
    s.paint("hat", robe, 0.5, skip=lambda f, x, y, w, h: f == "front" and 1 <= x <= 6 and y >= 2)
    s.art("head", "front", [
        "........", "........", ".dd..dd.", ".WC..CW.", ".CC..CC.", "........", "..dddd..", "........"],
        {"d": ((24, 14, 44), False), "W": (WH, True), "C": (CY, True)})
    for y in range(4):                                          # tay ao rach
        s.put("hat", "front", 1 + (y % 2), 2, robe[1])
    s.art("body", "front", [
        "..d..d..", "..dddd..", "...VV...", "..VddV..", "...VV...", "..dddd..",
        ".bbbbbb.", ".bYbbYb.", "........", "........", "........", "........"],
        {"d": ((24, 14, 44), False), "V": (VI, True), "b": ((30, 20, 20), False), "Y": (YE, False)})
    for a in ("rarm", "larm"):
        s.band(a, ("front", "back", "left", "right"), 2, 2, [(20, 12, 34), (60, 40, 100)])
        s.band(a, ("front", "back", "left", "right"), 5, 5, [(20, 12, 34), (60, 40, 100)])
        s.band(a, ("front", "back", "left", "right"), 10, 11, skin, 0.5)
        s.put(a, "front", 1, 7, VI, True)
    for l in ("rleg", "lleg"):
        s.band(l, ("front", "back", "left", "right"), 10, 11, [(6, 3, 12), (20, 12, 36)], 0.5)
    add_extras(s, "void_walker")
    s.save(os.path.join(ENTITY_DIR, "void_walker"))


# ------------------------------------------------------------------ Ke Rinh Rap
def phase_stalker():
    s = Skin(64, 64, 12)
    humanoid_parts(s)
    hide = [(18, 6, 28), (48, 14, 66), (98, 30, 120), (160, 66, 186)]
    s.paint("head", hide, 0.5)
    s.paint("body", hide, 0.42)
    for a in ("rarm", "larm"):
        s.paint(a, hide, 0.45)
    for l in ("rleg", "lleg"):
        s.paint(l, hide, 0.38)
    # long mao nhon tren dau (lop hat)
    for face in ("top", "back", "left", "right", "front"):
        fx, fy, fw, fh = s.rect("hat", face)
        for x in range(fw):
            hgt = 2 + (hash2(x, fy, 5) > 0.5) + (x % 3 == 0) if face != "front" else 1
            for y in range(int(hgt)):
                s.put("hat", face, x, y, ramp([(14, 4, 22), (40, 10, 56), (150, 50, 170)], 0.3 + 0.35 * y + 0.2 * hash2(x, y, 3)))
    s.art("head", "front", [
        "........", "........", ".d....d.", ".WP..PW.", "..PPPP..", "........", ".w.dd.w.", "..wwww.."],
        {"d": ((18, 6, 28), False), "W": (WH, True), "P": (MG, True), "w": ((240, 230, 245), False)})
    s.art("body", "front", [
        "P......P", ".P....P.", "..P..P..", "...PP...", "...PP...", "..P..P..",
        ".P....P.", "P......P", "........", "........", "........", "........"], {"P": (MG, True)})
    for a in ("rarm", "larm"):
        s.band(a, ("front", "back", "left", "right"), 9, 11, [(210, 200, 225), (250, 245, 255)], 0.6)
        for y in (2, 5, 8):
            s.put(a, "front", 1, y, MG, True)
            s.put(a, "back", 2, y, MG, True)
    for l in ("rleg", "lleg"):
        for y in range(1, 11):
            s.put(l, "left" if l == "rleg" else "right", 1, y, MG, True)
        s.band(l, ("front", "back", "left", "right"), 10, 11, [(6, 2, 10), (24, 8, 36)], 0.4)
    add_extras(s, "phase_stalker")
    s.save(os.path.join(ENTITY_DIR, "phase_stalker"))


# ------------------------------------------------------------------ Ho Phap
def rift_brute():
    s = Skin(64, 64, 13)
    humanoid_parts(s)
    rock = STONE_M
    s.paint("head", [(52, 44, 62), (96, 84, 110), (140, 124, 152), (186, 170, 196)], 0.5)
    s.paint("body", rock, 0.5)
    for a in ("rarm", "larm"):
        s.paint(a, rock, 0.5)
    for l in ("rleg", "lleg"):
        s.paint(l, rock, 0.42)
    # mu sat co sung (hat)
    s.paint("hat", [(30, 26, 42), (64, 58, 84), (108, 100, 132), (152, 144, 172)], 0.55,
            skip=lambda f, x, y, w, h: (f == "front" and (y >= 3 and not (x in (3, 4) and y <= 5))) or (y >= 4 and f != "top"))
    for x in (0, 7):                                            # sung
        s.put("hat", "left", x, 0, GOLD[2])
        s.put("hat", "right", x, 0, GOLD[2])
    s.art("head", "front", [
        "........", "........", "........", "..OO.OO.", ".OOO.OOO", "........", "..tddt..", "..t..t.."],
        {"O": (OR, True), "d": ((20, 14, 26), False), "t": ((236, 230, 214), False)})
    s.art("body", "front", [
        "pppppppp", "p..OO..p", "p.O..O.p", "p..OO..p", "p.O..O.p", "ppppppppp"[:8], "bbbbbbbb", "bYbbbbYb",
        "........", "........", "........", "........"],
        {"p": ((88, 80, 110), False), "O": (OR, True), "b": ((40, 28, 24), False), "Y": (YE, False)})
    for a in ("rarm", "larm"):
        s.band(a, ("front", "back", "left", "right", "top"), 0, 3, [(70, 64, 92), (130, 120, 156), (190, 180, 210)], 0.6)
        for x in (0, 3):
            s.put(a, "front", x, 3, (40, 36, 54))
        s.put(a, "front", 1, 6, OR, True)
        s.put(a, "front", 2, 7, OR, True)
        s.put(a, "back", 1, 8, OR, True)
    for l in ("rleg", "lleg"):
        s.put(l, "front", 1, 3, OR, True)
        s.put(l, "front", 2, 4, OR, True)
        s.put(l, "front", 2, 5, OR, True)
        s.band(l, ("front", "back", "left", "right"), 10, 11, [(24, 20, 34), (56, 50, 74)], 0.4)
    add_extras(s, "rift_brute")
    s.save(os.path.join(ENTITY_DIR, "rift_brute"))


# ------------------------------------------------------------------ Chua Te
def void_sovereign():
    s = Skin(64, 64, 14)
    humanoid_parts(s)
    obs = [(6, 3, 12), (16, 9, 30), (38, 22, 64), (78, 52, 118)]
    s.paint("head", [(20, 12, 34), (42, 28, 68), (80, 58, 124), (130, 104, 176)], 0.5)
    for p in ("body", "rarm", "larm", "rleg", "lleg"):
        s.paint(p, obs, 0.45)
    # vuong mien (hat)
    s.paint("hat", GOLD, 0.55, skip=lambda f, x, y, w, h: (f != "top" and y >= 2) or (f == "top" and 1 <= x <= w - 2 and 1 <= y <= h - 2))
    for f in ("front", "back", "left", "right"):
        fx, fy, fw, fh = s.rect("hat", f)
        for x in range(fw):
            if x % 2 == 1:
                s.put("hat", f, x, 0, None, clear=True)         # rang cua
        s.put("hat", f, 3, 1, MG, True)
    for (x, y) in ((0, 0), (7, 0), (0, 7), (7, 7)):
        s.put("hat", "top", x, y, MG, True)
    s.art("head", "front", [
        "........", "........", ".mm..mm.", ".MW..WM.", ".MM..MM.", "........", ".d.dd.d.", "........"],
        {"m": ((60, 20, 90), False), "M": (MG, True), "W": (WH, True), "d": ((6, 3, 12), False)})
    s.art("body", "front", [
        "gggggggg", "g.V..V.g", "g..VV..g", "g.VMMV.g", "g..MM..g", "g.V..V.g",
        "gggggggg", "gYYYYYYg", ".d.dd.d.", "........", "........", "........"],
        {"g": (GOLD[1], False), "V": (VI, True), "M": (MG, True), "Y": (GOLD[2], False), "d": ((6, 3, 12), False)})
    for a in ("rarm", "larm"):
        s.band(a, ("front", "back", "left", "right", "top"), 0, 2, GOLD, 0.6)
        s.band(a, ("front", "back", "left", "right"), 9, 10, GOLD, 0.5)
        for y in (4, 6):
            s.put(a, "front", 1, y, VI, True)
            s.put(a, "front", 2, y, VI, True)
    for l in ("rleg", "lleg"):
        s.band(l, ("front", "back", "left", "right"), 0, 1, GOLD, 0.55)
        s.band(l, ("front", "back", "left", "right"), 8, 11, GOLD, 0.45)
        s.put(l, "front", 1, 4, VI, True)
        s.put(l, "front", 2, 5, VI, True)
    add_extras(s, "void_sovereign")
    s.save(os.path.join(ENTITY_DIR, "void_sovereign"))


# ------------------------------------------------------------------ Cung thu (skeleton 64x32)
def rift_archer():
    s = Skin(64, 32, 15)
    s.part("head", 0, 0, 8, 8, 8)
    s.part("hat", 32, 0, 8, 8, 8)
    s.part("body", 16, 16, 8, 12, 4)
    s.part("rarm", 40, 16, 2, 12, 2)
    s.part("rleg", 0, 16, 2, 12, 2)
    bone = [(60, 54, 90), (112, 104, 150), (170, 164, 204), (222, 218, 240)]
    s.paint("head", bone, 0.55)
    s.paint("body", bone, 0.45)
    s.paint("rarm", bone, 0.5)
    s.paint("rleg", bone, 0.5)
    cloth = [(12, 10, 26), (28, 24, 54), (50, 44, 92), (78, 70, 130)]
    s.paint("hat", cloth, 0.5, skip=lambda f, x, y, w, h: (f == "front" and (y >= 2 and 1 <= x <= 6 or y >= 1 and 2 <= x <= 5)) or (f == "bottom"))
    for x in range(8):
        s.put("hat", "back", x, 5 + (x % 2) + (x % 3 == 0), cloth[1])
    s.art("head", "front", [
        "........", "........", ".kk..kk.", ".kC..Ck.", ".kk..kk.", "...nn...", ".tdtdtd.", ".dtdtdt."],
        {"k": ((14, 10, 26), False), "C": (CY, True), "n": ((60, 54, 80), False), "t": ((236, 232, 245), False), "d": ((40, 34, 60), False)})
    s.art("body", "front", [
        "...CC...", "ssssssss", "...CC...", "ssssssss", "...CC...", "ssssssss",
        "...CC...", ".ssssss.", "...CC...", "........", "........", "........"],
        {"s": ((46, 40, 70), False), "C": (CY, True)})
    s.put("rarm", "front", 0, 4, CY, True)
    s.put("rarm", "front", 1, 8, CY, True)
    s.band("rarm", ("front", "back", "left", "right"), 5, 5, [(40, 34, 60), (90, 82, 124)])
    s.band("rleg", ("front", "back", "left", "right"), 5, 5, [(40, 34, 60), (90, 82, 124)])
    add_extras(s, "rift_archer")
    s.save(os.path.join(ENTITY_DIR, "rift_archer"))


# ------------------------------------------------------------------ Lon rung (pig 64x32)
def void_boar():
    s = Skin(64, 32, 16)
    s.part("head", 0, 0, 8, 8, 8)
    s.part("body", 28, 8, 10, 16, 8)
    s.part("snout", 16, 16, 4, 3, 1)
    s.part("leg", 0, 16, 4, 6, 4)
    fur = [(22, 14, 36), (46, 30, 72), (80, 54, 118), (122, 90, 164)]
    s.paint("head", fur, 0.5)
    s.paint("body", fur, 0.45)
    s.paint("leg", fur, 0.35)
    s.paint("snout", [(70, 40, 90), (130, 84, 150), (186, 140, 200), (226, 190, 236)], 0.5)
    s.art("head", "front", [
        "........", "........", ".dd..dd.", ".CC..CC.", "........", "........", "t......t", "t......t"],
        {"d": ((10, 6, 18), False), "C": (CY, True), "t": ((240, 232, 214), False)})
    s.art("snout", "front", ["....", ".dd.", "...."], {"d": ((24, 10, 34), False)})
    # song lung phat sang: lung heo la mat 'back' cua khoi than (10 x 16)
    fx, fy, fw, fh = s.rect("body", "back")
    for y in range(fh):
        for x in range(4, 6):
            s.put("body", "back", x, y, ramp([(70, 46, 110), (130, 96, 176), (190, 160, 230)], 0.5 + 0.3 * hash2(x, y, 9)))
    for y in (2, 6, 10, 14):
        for x in (4, 5):
            s.put("body", "back", x, y, VI, True)
        s.put("body", "back", 4, y - 1 if y > 0 else y, CY, True)
    s.band("leg", ("front", "back", "left", "right"), 5, 5, [(10, 6, 18), (30, 20, 46)], 0.4)
    add_extras(s, "void_boar")
    s.save(os.path.join(ENTITY_DIR, "void_boar"))


# ------------------------------------------------------------------ Giap mac tren nguoi
def armor(name, cols, trim, trim_glow, cloth, seed):
    light = cols
    s1 = Skin(64, 32, seed)
    s1.part("head", 0, 0, 8, 8, 8)
    s1.part("body", 16, 16, 8, 12, 4)
    s1.part("rarm", 40, 16, 4, 12, 4)
    s1.part("rleg", 0, 16, 4, 12, 4)
    s1.paint("head", light, 0.55, skip=lambda f, x, y, w, h: f == "front" and 1 <= x <= 6 and 4 <= y <= 5 and False)
    s1.paint("body", light, 0.5)
    s1.paint("rarm", light, 0.5)
    s1.paint("rleg", light, 0.45, skip=lambda f, x, y, w, h: f in ("top",) or (y < h - 5 and f != "bottom") or f == "bottom" and False)
    s1.band("head", ("front", "back", "left", "right"), 0, 1, trim, 0.5)
    s1.art("head", "front", [
        "........", "........", "........", ".tt..tt.", ".TT..TT.", "........", "........", "........"],
        {"t": (trim[1], False), "T": (trim[3], trim_glow)})
    s1.art("body", "front", [
        "tttttttt", "t..TT..t", "t.T..T.t", "t..TT..t", "t......t", "tttttttt", "........", "........",
        "........", "........", "........", "........"], {"t": (trim[1], False), "T": (trim[3], trim_glow)})
    s1.band("rarm", ("front", "back", "left", "right", "top"), 0, 2, trim, 0.55)
    s1.band("rarm", ("front", "back", "left", "right"), 9, 11, trim, 0.4)
    s1.band("rleg", ("front", "back", "left", "right"), 8, 8, trim, 0.55)
    s1.put("head", "front", 3, 4, trim[3], False)
    s1.save(os.path.join(ARMOR_DIR, name + "_layer_1"), glow=False)

    s2 = Skin(64, 32, seed + 1)
    s2.part("body", 16, 16, 8, 12, 4)
    s2.part("rleg", 0, 16, 4, 12, 4)
    s2.paint("body", light, 0.45, skip=lambda f, x, y, w, h: y < h - 5 or f in ("top",))
    s2.paint("rleg", light, 0.45)
    s2.band("body", ("front", "back", "left", "right"), 7, 7, trim, 0.55)
    s2.art("body", "front", [
        "........", "........", "........", "........", "........", "........", "........",
        "tTTTTTTt", ".tTtTTt.", "........", "........", "........"], {"t": (trim[1], False), "T": (trim[3], trim_glow)})
    s2.band("rleg", ("front", "back", "left", "right"), 0, 0, trim, 0.55)
    s2.band("rleg", ("front", "back", "left", "right"), 5, 6, trim, 0.5)
    s2.put("rleg", "front", 1, 3, trim[3], False)
    s2.put("rleg", "front", 2, 3, trim[3], False)
    s2.save(os.path.join(ARMOR_DIR, name + "_layer_2"), glow=False)


# ------------------------------------------------------------------ Khoi dong (animated)
def write_anim(name, frames, frametime, interpolate=True):
    sheet = Image.new("RGBA", (16, 16 * len(frames)), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        sheet.paste(fr, (0, 16 * i))
    path = os.path.join(BLOCK_DIR, name + ".png")
    sheet.save(path)
    with open(path + ".mcmeta", "w") as f:
        json.dump({"animation": {"frametime": frametime, "interpolate": interpolate}}, f)


def stone_base(cols, seed, scale=3.0):
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            n = 0.6 * vnoise(x, y, scale, seed) + 0.4 * hash2(x, y, seed + 5)
            im.putpixel((x, y), ramp(cols, 0.25 + n * 0.6))
    return im


def ore_frames(base_cols, seed):
    base = stone_base(base_cols, seed)
    clusters = [(3, 3), (10, 3), (5, 10), (12, 11), (8, 7)]
    frames = []
    N = 8
    for f in range(N):
        im = base.copy()
        for k, (cx, cy) in enumerate(clusters):
            pulse = 0.5 + 0.5 * math.sin(2 * math.pi * (f / N + k * 0.21))
            body = [(50, 28, 120), (96, 60, 200), (150, 110, 255), (205, 180, 255)]
            shape = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (-1, 1), (2, 2)]
            for i, (dx, dy) in enumerate(shape):
                t = 0.25 + 0.2 * (dx + 1) / 3 - 0.05 * dy + 0.3 * pulse * (1 if i < 3 else 0.4)
                im.putpixel((cx + dx, cy + dy), ramp(body, t))
            im.putpixel((cx, cy), ramp(body, 0.75 + 0.25 * pulse))
            if (f + k * 2) % N == 0:                              # lap lanh
                for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
                    x, y = cx + dx, cy + dy
                    if 0 <= x < 16 and 0 <= y < 16:
                        im.putpixel((x, y), (235, 220, 255, 255))
                im.putpixel((cx, cy), (255, 255, 255, 255))
        frames.append(im)
    return frames


def steel_block_frames():
    frames = []
    N = 8
    for f in range(N):
        im = Image.new("RGBA", (16, 16))
        pulse = 0.5 + 0.5 * math.sin(2 * math.pi * f / N)
        cols = [(30, 18, 60), (62, 40, 120), (104, 76, 180), (158, 128, 230)]
        for y in range(16):
            for x in range(16):
                n = hash2(x, y, 31)
                t = 0.45 + (n - 0.5) * 0.12
                if x in (0, 15) or y in (0, 15):
                    t = 0.05
                elif x == 1 or y == 1:
                    t = 0.95
                elif x == 14 or y == 14:
                    t = 0.2
                im.putpixel((x, y), ramp(cols, t))
        for i in range(3, 13):                                     # ranh + van phat sang
            for (x, y) in ((i, 8), (8, i)):
                glow = 0.45 + 0.55 * pulse * (1 - abs(i - 8) / 6)
                im.putpixel((x, y), ramp([(40, 90, 120), (110, 220, 255), (230, 255, 255)], glow))
        for (x, y) in ((4, 4), (11, 4), (4, 11), (11, 11)):
            im.putpixel((x, y), ramp([(90, 170, 220), (200, 250, 255)], 0.4 + 0.6 * pulse))
            im.putpixel((x + 1, y), (30, 18, 60, 255))
        frames.append(im)
    return frames


def void_stone_frames():
    base = stone_base([(8, 5, 18), (20, 12, 40), (38, 24, 70), (60, 42, 104)], 41, 4.0)
    stars = [(hash2(i, 1, 77), (int(hash2(i, 2, 77) * 16), int(hash2(i, 3, 77) * 16))) for i in range(11)]
    frames = []
    N = 8
    for f in range(N):
        im = base.copy()
        for i, (ph, (x, y)) in enumerate(stars):
            tw = 0.5 + 0.5 * math.sin(2 * math.pi * (f / N + ph))
            im.putpixel((x, y), ramp([(60, 40, 110), (150, 110, 240), (235, 220, 255)], 0.2 + 0.8 * tw))
        frames.append(im)
    return frames


def lantern_frames():
    frames = []
    N = 8
    for f in range(N):
        im = Image.new("RGBA", (16, 16))
        ang0 = 2 * math.pi * f / N
        for y in range(16):
            for x in range(16):
                dx, dy = x - 7.5, y - 7.5
                d = math.hypot(dx, dy)
                frame = x in (0, 1, 14, 15) or y in (0, 1, 14, 15)
                if frame:
                    t = 0.15 + (0.35 if (x in (0, 15) or y in (0, 15)) else 0.0)
                    im.putpixel((x, y), ramp([(14, 8, 30), (50, 32, 96), (100, 70, 170)], t if (x + y) % 2 else t * 0.8))
                    continue
                a = math.atan2(dy, dx) - ang0
                swirl = 0.5 + 0.5 * math.sin(3 * a + d * 0.9)
                glow = max(0.0, 1 - d / 7.5)
                t = min(1.0, 0.25 * swirl + 0.85 * glow)
                im.putpixel((x, y), ramp([(60, 14, 90), (200, 50, 200), (255, 130, 240), (255, 250, 255)], t))
        for (x, y) in ((1, 1), (14, 1), (1, 14), (14, 14)):
            im.putpixel((x, y), (150, 230, 255, 255))
        frames.append(im)
    return frames


def void_bricks_static():
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            row = y // 4
            off = 0 if row % 2 == 0 else 4
            mortar = (y % 4 == 3) or ((x + off) % 8 == 7)
            n = 0.55 * vnoise(x, y, 3, 52) + 0.45 * hash2(x, y, 53)
            if mortar:
                im.putpixel((x, y), ramp([(6, 4, 12), (16, 10, 30)], n))
            else:
                t = 0.35 + n * 0.5
                if y % 4 == 0:
                    t += 0.15
                im.putpixel((x, y), ramp([(22, 16, 40), (44, 32, 76), (74, 56, 120), (104, 84, 158)], t))
    rng = random.Random(5)
    for _ in range(7):                                               # ranh nut phat sang
        x, y = rng.randrange(16), rng.randrange(16)
        if im.getpixel((x, y))[0] > 20:
            im.putpixel((x, y), ramp([(80, 50, 170), (160, 110, 255)], rng.random()))
    return im


def make_blocks():
    write_anim("void_crystal_ore", ore_frames([(92, 92, 98), (124, 124, 130), (156, 156, 162), (188, 188, 194)], 21), 5)
    write_anim("deepslate_void_crystal_ore", ore_frames([(30, 30, 36), (52, 52, 60), (78, 78, 88), (102, 102, 114)], 22), 5)
    write_anim("void_steel_block", steel_block_frames(), 6)
    write_anim("void_stone", void_stone_frames(), 8)
    write_anim("rift_lantern", lantern_frames(), 3)
    void_bricks_static().save(os.path.join(BLOCK_DIR, "void_bricks.png"))
    for n in ("void_bricks",):
        p = os.path.join(BLOCK_DIR, n + ".png.mcmeta")
        if os.path.exists(p):
            os.remove(p)


# ------------------------------------------------------------------ Polish icon vat pham
def polish_item(path):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    src = im.copy()

    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and src.getpixel((x, y))[3] > 40

    def is_outline(c):
        return c[3] > 40 and c[0] < 40 and c[1] < 30 and c[2] < 60

    for y in range(h):
        for x in range(w):
            c = src.getpixel((x, y))
            if c[3] < 40:
                continue
            if is_outline(c):
                # vien chon loc: lay mau ke can toi di, ngả tim
                neigh = [src.getpixel((x + dx, y + dy)) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                         if opaque(x + dx, y + dy) and not is_outline(src.getpixel((x + dx, y + dy)))]
                if neigh:
                    r = sum(n[0] for n in neigh) / len(neigh)
                    gr = sum(n[1] for n in neigh) / len(neigh)
                    b = sum(n[2] for n in neigh) / len(neigh)
                    im.putpixel((x, y), (int(r * 0.30 + 8), int(gr * 0.22 + 4), int(b * 0.40 + 16), 255))
                continue
            up, left = not opaque(x, y - 1) or is_outline(src.getpixel((x, y - 1))), not opaque(x - 1, y) or is_outline(src.getpixel((x - 1, y)))
            dn, rt = not opaque(x, y + 1) or is_outline(src.getpixel((x, y + 1))), not opaque(x + 1, y) or is_outline(src.getpixel((x + 1, y)))
            f = 1.0
            if up or left:
                f *= 1.16
            if dn or rt:
                f *= 0.84
            if f != 1.0:
                im.putpixel((x, y), (min(255, int(c[0] * f + (6 if f > 1 else 0))), min(255, int(c[1] * f)), min(255, int(c[2] * f + (10 if f > 1 else 0))), c[3]))
    im.save(path)


def make_items():
    g.make_items()
    for fn in sorted(os.listdir(ITEM_DIR)):
        if fn.endswith(".png"):
            polish_item(os.path.join(ITEM_DIR, fn))


# ------------------------------------------------------------------ Phan 3D them cho quai (sinh Java + texture)
EXTRAS = {}          # mob -> [dict]
ARM_PARENTS = {"right_arm": "left_arm", "right_leg": "left_leg"}
ROBE = [(10, 6, 20), (24, 14, 44), (48, 30, 86), (84, 58, 140)]
HIDE = [(18, 6, 28), (48, 14, 66), (98, 30, 120), (160, 66, 186)]
OBSID = [(6, 3, 12), (16, 9, 30), (38, 22, 64), (78, 52, 118)]
VIOL = [(60, 30, 130), (130, 80, 230), (190, 150, 255), (240, 225, 255)]
PINK = [(120, 20, 110), (230, 60, 200), (255, 150, 235), (255, 235, 255)]
CYANR = [(30, 110, 150), (80, 200, 240), (160, 240, 255), (240, 255, 255)]
IVORY = [(120, 108, 92), (180, 168, 148), (226, 218, 198), (250, 246, 232)]
LEATH = [(30, 18, 16), (66, 40, 30), (104, 66, 44), (140, 96, 64)]
CLOTH = [(12, 10, 26), (28, 24, 54), (50, 44, 92), (78, 70, 130)]
BONEC = [(60, 54, 90), (112, 104, 150), (170, 164, 204), (222, 218, 240)]
FURC = [(22, 14, 36), (46, 30, 72), (80, 54, 118), (122, 90, 164)]


def ex(s, mob, parent, name, size, origin, pose, rot=(0, 0, 0), ramp=ROBE, base=0.5, glow=False,
       twin=False, uv_of=None, fn=None):
    w, h, d = size
    if uv_of:
        u, v = EXTRAS_UV[(mob, uv_of)]
    else:
        u, v = s.alloc(name, w, h, d)
        s.paint(name, ramp, base)
        if fn:
            fn(s, name)
        if glow:
            s.glow_part(name)
    EXTRAS_UV[(mob, name)] = (u, v)
    EXTRAS.setdefault(mob, []).append(dict(parent=parent, name=name, u=u, v=v, size=size, origin=origin,
                                           pose=pose, rot=rot, mirror=False))
    if twin:
        tp = ARM_PARENTS.get(parent, parent)
        EXTRAS[mob].append(dict(parent=tp, name=name + "_l", u=u, v=v, size=size, origin=origin,
                                pose=(-pose[0], pose[1], pose[2]), rot=(rot[0], -rot[1], -rot[2]), mirror=True))


EXTRAS_UV = {}


def trim_gold(rows):
    def fn(s, name):
        for face in ("front", "back", "left", "right"):
            s.band(name, (face,), rows[0], rows[1], GOLD, 0.6)
    return fn


def add_extras(s, mob):
    if mob == "void_walker":
        ex(s, mob, "head", "hood_peak", (4, 3, 5), (-2, -1.5, -0.5), (0, -8.2, 2.0), (-25, 0, 0), ROBE, 0.5)
        ex(s, mob, "body", "cloak", (10, 14, 1), (-5, 0, 0), (0, 0.5, 2.3), (4, 0, 0), ROBE, 0.4)
        ex(s, mob, "body", "cloak_hem", (10, 5, 1), (-5, 0, 0), (0, 14.3, 2.6), (8, 0, 0), ROBE, 0.3)
        ex(s, mob, "body", "shard", (1, 3, 1), (-0.5, -1.5, -0.5), (8.5, -3, 0), (0, 0, 15), VIOL, 0.6, glow=True, twin=True)
    elif mob == "phase_stalker":
        ex(s, mob, "head", "crest_a", (1, 4, 1), (-0.5, -4, -0.5), (0, -8, -1), (-20, 0, 0), HIDE, 0.6)
        ex(s, mob, "head", "crest_b", (1, 5, 1), (-0.5, -5, -0.5), (0, -8, 1), (-35, 0, 0), HIDE, 0.6)
        ex(s, mob, "head", "crest_c", (1, 5, 1), (-0.5, -5, -0.5), (0, -8, 3), (-50, 0, 0), PINK, 0.5, glow=True)
        for i, (py, rx) in enumerate(((1.0, 35), (4.5, 40), (8.0, 50))):
            ex(s, mob, "body", f"spine_{i}", (1, 5, 1), (-0.5, 0, 0), (0, py, 2.2), (rx, 0, 0), PINK, 0.45, glow=True,
               uv_of="spine_0" if i else None)
        ex(s, mob, "body", "tail_a", (2, 2, 7), (-1, 0, 0), (0, 10.5, 2), (25, 0, 0), HIDE, 0.5)
        ex(s, mob, "body", "tail_b", (1, 1, 5), (-0.5, 0, 0), (0, 12.5, 8), (40, 0, 0), PINK, 0.5, glow=True)
        for i, dx in enumerate((-1.5, 0.0, 1.5)):
            ex(s, mob, "right_arm", f"claw_{i}", (1, 4, 1), (-0.5, 0, -0.5), (-1 + dx, 12, 0), (-10, 0, 0), IVORY, 0.55,
               twin=True, uv_of="claw_0" if i else None)
    elif mob == "rift_brute":
        ex(s, mob, "head", "horn_base", (2, 4, 2), (-1, -4, -1), (4.3, -7.5, 0), (0, 0, -28), IVORY, 0.5, twin=True)
        ex(s, mob, "head", "horn_tip", (1, 3, 1), (-0.5, -3, -0.5), (6.4, -11, 0), (0, 0, -50), IVORY, 0.65, twin=True)
        ex(s, mob, "right_arm", "pauldron", (6, 2, 6), (-3, -1, -3), (-1, -1.5, 0), (0, 0, 0), STONE_M, 0.6, twin=True)
        ex(s, mob, "right_arm", "p_spike", (1, 3, 1), (-0.5, -3, -0.5), (-1, -3, 0), (0, 0, 0), STONE_M, 0.7, twin=True)
        ex(s, mob, "right_arm", "fist", (5, 3, 5), (-2.5, 0, -2.5), (-1, 10, 0), (0, 0, 0), STONE_M, 0.45, twin=True,
           fn=lambda s_, n: s_.band(n, ("front", "back", "left", "right"), 2, 2, [(40, 20, 8), OR], 0.7))
        ex(s, mob, "body", "back_plate", (7, 8, 1), (-3.5, 0, 0), (0, 0.5, 2.2), (0, 0, 0), STONE_M, 0.55)
        for i, (px, py) in enumerate(((-2.5, 3.0), (0.0, 6.0), (2.5, 3.0))):
            ex(s, mob, "body", f"b_spike_{i}", (1, 1, 3), (-0.5, -0.5, 0), (px, py, 3.2), (0, 0, 0), STONE_M, 0.7,
               uv_of="b_spike_0" if i else None)
        ex(s, mob, "body", "skirt", (8, 2, 4), (-4, 0, -2), (0, 10.5, 0), (0, 0, 0), [(24, 20, 34), (56, 50, 74), (90, 82, 112), (130, 120, 156)], 0.5)
    elif mob == "void_sovereign":
        for i, (px, pz) in enumerate(((0, -3.6), (3.4, -3.4), (-3.4, -3.4), (0, 3.6), (3.4, 3.4), (-3.4, 3.4))):
            ex(s, mob, "head", f"cspike_{i}", (1, 3, 1), (-0.5, -3, -0.5), (px, -8.2, pz), (0, 0, 0), GOLD, 0.6,
               uv_of="cspike_0" if i else None)
        ex(s, mob, "head", "horn_1", (2, 5, 2), (-1, -5, -1), (3.2, -8, 0), (0, 0, -20), OBSID, 0.5, twin=True)
        ex(s, mob, "head", "horn_2", (2, 4, 2), (-1, -4, -1), (5.4, -12.6, 0), (0, 0, -45), OBSID, 0.5, twin=True)
        ex(s, mob, "head", "horn_3", (1, 3, 1), (-0.5, -3, -0.5), (8.6, -15.2, 0), (0, 0, -75), PINK, 0.5, glow=True, twin=True)
        ex(s, mob, "body", "cape", (10, 14, 1), (-5, 0, 0), (0, 0.5, 2.4), (5, 0, 0), OBSID, 0.4)
        ex(s, mob, "body", "cape_low", (10, 8, 1), (-5, 0, 0), (0, 14.2, 3.6), (10, 0, 0), OBSID, 0.35,
           fn=lambda s_, n: s_.band(n, ("front", "back"), 7, 7, GOLD, 0.6))
        ex(s, mob, "right_arm", "sh_spike", (1, 4, 1), (-0.5, -4, -0.5), (-1, -2, 0), (0, 0, 20), GOLD, 0.6, twin=True)
        ex(s, mob, "body", "blade_a", (1, 10, 2), (-0.5, -10, -1), (3.5, 3, 3.5), (0, 0, -25), VIOL, 0.55, glow=True, twin=True)
        ex(s, mob, "body", "blade_b", (1, 8, 2), (-0.5, -8, -1), (3.5, 5, 3.2), (0, 0, -55), VIOL, 0.45, glow=True, twin=True)
        ex(s, mob, "body", "core_gem", (4, 4, 1), (-2, 0, -0.5), (0, 3, -2.3), (0, 0, 0), PINK, 0.6, glow=True)
    elif mob == "rift_archer":
        ex(s, mob, "head", "hood_tip", (4, 3, 4), (-2, -1.5, -0.5), (0, -8.3, 1.5), (-20, 0, 0), CLOTH, 0.5)
        ex(s, mob, "body", "quiver", (2, 6, 2), (-1, 0, 0), (2.5, 1, 2.8), (0, 0, 10), LEATH, 0.5)
        for i, dx in enumerate((1.5, 3.5)):
            ex(s, mob, "body", f"arrow_{i}", (1, 3, 1), (-0.5, -3, -0.5), (dx, 1.2, 3.0), (0, 0, 10), CYANR, 0.6,
               glow=(i == 0), uv_of="arrow_0" if i else None)
        ex(s, mob, "body", "scarf_tail", (2, 6, 1), (-1, 0, 0), (3, 0.5, 3.2), (8, 0, 0), CLOTH, 0.5)
    elif mob == "void_boar":
        ex(s, mob, "head", "tusk_a", (1, 1, 3), (-0.5, -0.5, -1.5), (3, 2.5, -9.5), (0, 0, 0), IVORY, 0.55, twin=True)
        ex(s, mob, "head", "tusk_b", (1, 3, 1), (-0.5, -3, -0.5), (3, 2.2, -11), (-15, 0, 0), IVORY, 0.65, twin=True)
        ex(s, mob, "head", "crest", (2, 2, 4), (-1, -2, -2), (0, -3.8, -4), (0, 0, 0), FURC, 0.6)
        for i, (py, sz) in enumerate(((-6, (2, 2, 4)), (-1, (2, 2, 3)), (4, (2, 2, 4)))):
            ex(s, mob, "body", f"crystal_{i}", sz, (-sz[0] / 2, -sz[1] / 2, 0), (0, py, 1), (10 if i == 1 else -10, 0, 0),
               VIOL, 0.6, glow=True)


def java_f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".") + "F" if v != int(v) else "%d.0F" % int(v)


def write_java():
    def lines(mob):
        out = []
        for e in EXTRAS.get(mob, []):
            w, h, d = e["size"]
            ox, oy, oz = e["origin"]
            if e["mirror"]:
                ox = -ox - w
            px, py, pz = e["pose"]
            rx, ry, rz = e["rot"]
            cube = "CubeListBuilder.create().texOffs(%d, %d)%s.addBox(%s, %s, %s, %s, %s, %s)" % (
                e["u"], e["v"], ".mirror()" if e["mirror"] else "", java_f(ox), java_f(oy), java_f(oz),
                java_f(w), java_f(h), java_f(d))
            pose = "PartPose.offsetAndRotation(%s, %s, %s, r(%s), r(%s), r(%s))" % (
                java_f(px), java_f(py), java_f(pz), java_f(rx), java_f(ry), java_f(rz))
            out.append('        root.getChild("%s").addOrReplaceChild("%s", %s, %s);' % (e["parent"], e["name"], cube, pose))
        return "\n".join(out)

    humanoid = """    public static LayerDefinition %s() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();
%s
        return LayerDefinition.create(mesh, 64, 64);
    }
"""
    src = """package com.voidrealm.mod.client;

import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.QuadrupedModel;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;

/**
 * DO TOOLS/gen_art.py SINH RA - khong sua tay. Model 3D rieng cua quai: giu khung vanilla (nhe)
 * va gan them sung, mu, ao choang, canh, duoi, nanh... vao cac bo phan co san.
 */
public final class ModelExtras {
    private static float r(float degrees) {
        return (float) Math.toRadians(degrees);
    }

""" + humanoid % ("voidWalker", lines("void_walker")) + "\n" + humanoid % ("phaseStalker", lines("phase_stalker")) \
        + "\n" + humanoid % ("riftBrute", lines("rift_brute")) + "\n" + humanoid % ("voidSovereign", lines("void_sovereign")) + """
    public static LayerDefinition riftArcher() {
        MeshDefinition mesh = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("right_arm", CubeListBuilder.create().texOffs(40, 16).addBox(-1.0F, -2.0F, -1.0F, 2.0F, 12.0F, 2.0F), PartPose.offset(-5.0F, 2.0F, 0.0F));
        root.addOrReplaceChild("left_arm", CubeListBuilder.create().texOffs(40, 16).mirror().addBox(-1.0F, -2.0F, -1.0F, 2.0F, 12.0F, 2.0F), PartPose.offset(5.0F, 2.0F, 0.0F));
        root.addOrReplaceChild("right_leg", CubeListBuilder.create().texOffs(0, 16).addBox(-1.0F, 0.0F, -1.0F, 2.0F, 12.0F, 2.0F), PartPose.offset(-2.0F, 12.0F, 0.0F));
        root.addOrReplaceChild("left_leg", CubeListBuilder.create().texOffs(0, 16).mirror().addBox(-1.0F, 0.0F, -1.0F, 2.0F, 12.0F, 2.0F), PartPose.offset(2.0F, 12.0F, 0.0F));
""" + lines("rift_archer") + """
        return LayerDefinition.create(mesh, 64, 32);
    }

    public static LayerDefinition voidBoar() {
        MeshDefinition mesh = QuadrupedModel.createBodyMesh(6, CubeDeformation.NONE);
        PartDefinition root = mesh.getRoot();
        root.addOrReplaceChild("head", CubeListBuilder.create().texOffs(0, 0).addBox(-4.0F, -4.0F, -8.0F, 8.0F, 8.0F, 8.0F)
                .texOffs(16, 16).addBox(-2.0F, 0.0F, -9.0F, 4.0F, 3.0F, 1.0F), PartPose.offset(0.0F, 12.0F, -6.0F));
""" + lines("void_boar") + """
        return LayerDefinition.create(mesh, 64, 32);
    }

    private ModelExtras() {
    }
}
"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "java", "com", "voidrealm", "mod", "client", "ModelExtras.java")
    open(path, "w", encoding="utf-8").write(src)


if __name__ == "__main__":
    make_items()
    make_blocks()
    void_walker()
    phase_stalker()
    rift_brute()
    void_sovereign()
    rift_archer()
    void_boar()
    armor("void_steel", [(18, 10, 40), (50, 32, 104), (96, 68, 176), (160, 130, 240)],
          [(60, 150, 190), (120, 224, 255), (190, 246, 255), (255, 255, 255)], False, False, 40)
    armor("phase_cloth", [(60, 18, 78), (118, 44, 150), (186, 92, 214), (240, 160, 255)],
          [(150, 40, 130), (255, 92, 225), (255, 160, 240), (255, 240, 255)], False, True, 50)
    write_java()
    print("Da sinh do hoa nang cap")
