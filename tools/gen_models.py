#!/usr/bin/env python3
"""Sinh model 3D (elements JSON) + texture sheet cho vu khi, vat pham, den Khe Nut va quang.
Chay SAU gen_data.py:  python3 tools/gen_models.py
Vu khi cam tay duoc thiet ke thang dung roi xoay -45 do quanh truc Z cho khop voi
tu the 'handheld' cua vanilla (tay cam o duoi-trai, mui o tren-phai).
Neu khi vao game vu khi bi nghieng nguoc, doi DIAG thanh +45.
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_art as A  # noqa: E402
from PIL import Image  # noqa: E402

DIAG = -45
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources", "assets", "voidrealm")
ITEM_TEX = os.path.join(ROOT, "textures", "item", "model")
BLOCK_TEX = os.path.join(ROOT, "textures", "block", "model")
for d in (ITEM_TEX, BLOCK_TEX):
    os.makedirs(d, exist_ok=True)

STEEL = [(20, 12, 44), (52, 34, 110), (100, 74, 180), (170, 142, 245)]
STEEL_LT = [(52, 40, 110), (104, 84, 190), (168, 150, 244), (230, 222, 255)]
DARKM = [(18, 10, 24), (40, 22, 52), (70, 44, 90), (110, 76, 130)]
ORANGE_R = [(150, 60, 10), (255, 140, 40), (255, 200, 110), (255, 245, 200)]
GREEN_R = [(20, 70, 60), (50, 150, 120), (110, 220, 170), (200, 255, 230)]
APPLE = [(40, 10, 70), (96, 24, 130), (170, 50, 190), (240, 130, 240)]
SILK_R = [(150, 60, 170), (230, 120, 240), (255, 190, 255), (255, 245, 255)]

HAND_DISPLAY = {
    "thirdperson_righthand": {"rotation": [0, -90, 55], "translation": [0, 4.0, 0.5], "scale": [0.85, 0.85, 0.85]},
    "thirdperson_lefthand": {"rotation": [0, 90, -55], "translation": [0, 4.0, 0.5], "scale": [0.85, 0.85, 0.85]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "gui": {"rotation": [8, -22, 0], "translation": [0, 0, 0], "scale": [0.95, 0.95, 0.95]},
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "fixed": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [1, 1, 1]},
}
OBJ_DISPLAY = {
    "thirdperson_righthand": {"rotation": [0, 0, 0], "translation": [0, 3, 1], "scale": [0.55, 0.55, 0.55]},
    "thirdperson_lefthand": {"rotation": [0, 0, 0], "translation": [0, 3, 1], "scale": [0.55, 0.55, 0.55]},
    "firstperson_righthand": {"rotation": [0, -90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "firstperson_lefthand": {"rotation": [0, 90, -25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
    "gui": {"rotation": [28, 215, 0], "translation": [0, 0, 0], "scale": [0.95, 0.95, 0.95]},
    "ground": {"rotation": [0, 0, 0], "translation": [0, 3, 0], "scale": [0.5, 0.5, 0.5]},
    "head": {"rotation": [0, 180, 0], "translation": [0, 13, 7], "scale": [1, 1, 1]},
    "fixed": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [0.9, 0.9, 0.9]},
}
FACE_MAP = {"north": "front", "south": "back", "west": "right", "east": "left", "up": "top", "down": "bottom"}


class Model:
    def __init__(self, name, diag, tex_dir, tex_prefix, seed=1, k=2):
        self.name, self.diag, self.tex_dir, self.tex_prefix, self.k = name, diag, tex_dir, tex_prefix, k
        self.seed = seed
        self.boxes = []

    def b(self, name, x0, x1, y0, y1, z0, z1, ramp, base=0.5, glow=False, fn=None, share=None, rot=None):
        self.boxes.append(dict(name=name, a=(x0, y0, z0), b=(x1, y1, z1), ramp=ramp, base=base, glow=glow,
                               fn=fn, share=share, rot=rot))

    def sym(self, name, x0, x1, y0, y1, z0, z1, ramp, base=0.5, glow=False, fn=None):
        """Hai ban doi xung qua x=0 (x0,x1 >= 0)."""
        self.b(name + "_r", x0, x1, y0, y1, z0, z1, ramp, base, glow, fn)
        self.b(name + "_l", -x1, -x0, y0, y1, z0, z1, ramp, base, glow, share=name + "_r")

    def build(self):
        for size in (64, 96, 128):
            try:
                return self._build(size)
            except RuntimeError:
                continue
        raise RuntimeError("model qua lon: " + self.name)

    def _build(self, size):
        s = A.Skin(size, size, self.seed)
        uvs, elements = {}, []
        for bx in self.boxes:
            (x0, y0, z0), (x1, y1, z1) = bx["a"], bx["b"]
            W, H, D = (max(1, round((x1 - x0) * self.k)), max(1, round((y1 - y0) * self.k)),
                       max(1, round((z1 - z0) * self.k)))
            if bx["share"]:
                u, v, W, H, D = uvs[bx["share"]]
            else:
                u, v = s.alloc(bx["name"], W, H, D)
                s.paint(bx["name"], bx["ramp"], bx["base"])
                if bx["fn"]:
                    bx["fn"](s, bx["name"])
            uvs[bx["name"]] = (u, v, W, H, D)
            fc = A.faces(u, v, W, H, D)
            faces = {}
            for mc, nm in FACE_MAP.items():
                fx, fy, fw, fh = fc[nm]
                faces[mc] = {"uv": [round(fx * 16 / size, 4), round(fy * 16 / size, 4),
                                    round((fx + fw) * 16 / size, 4), round((fy + fh) * 16 / size, 4)], "texture": "#0"}
            el = {"from": [8 + x0, y0, 8 + z0], "to": [8 + x1, y1, 8 + z1], "faces": faces}
            if self.diag:
                el["rotation"] = {"origin": [8, 8, 8], "axis": "z", "angle": DIAG}
            elif bx["rot"]:
                axis, ang = bx["rot"][0], bx["rot"][1]
                origin = bx["rot"][2] if len(bx["rot"]) > 2 else [8 + (x0 + x1) / 2, (y0 + y1) / 2, 8 + (z0 + z1) / 2]
                el["rotation"] = {"origin": origin, "axis": axis, "angle": ang}
            if bx["glow"]:
                el["shade"] = False
                el["neoforge_data"] = {"block_light": 15, "sky_light": 15}
            elements.append(el)
        s.img.save(os.path.join(self.tex_dir, self.name + ".png"))
        return elements

    def write_item(self):
        elements = self.build()
        tex = "voidrealm:%s/%s" % (self.tex_prefix, self.name)
        obj = {"textures": {"0": tex, "particle": tex}, "elements": elements,
               "display": HAND_DISPLAY if self.diag else OBJ_DISPLAY}
        with open(os.path.join(ROOT, "models", "item", self.name + ".json"), "w") as f:
            json.dump(obj, f, indent=1)
        return len(elements)

    def write_block(self, particle):
        elements = self.build()
        tex = "voidrealm:%s/%s" % (self.tex_prefix, self.name)
        obj = {"parent": "minecraft:block/block", "textures": {"0": tex, "particle": particle}, "elements": elements}
        with open(os.path.join(ROOT, "models", "block", self.name + ".json"), "w") as f:
            json.dump(obj, f, indent=1)
        return len(elements)


def tex_rows(rows, ramp2, faces_=("front", "back", "left", "right")):
    def fn(s, name):
        for r0, r1 in rows:
            s.band(name, faces_, r0, r1, ramp2, 0.5)
    return fn


# ------------------------------------------------------------------ vu khi cam tay
def sword():
    m = Model("void_steel_sword", True, ITEM_TEX, "item/model", 101)
    m.b("pommel", -1.5, 1.5, -3, -1, -1.5, 1.5, STEEL, 0.4)
    m.b("pgem", -0.8, 0.8, -2.6, -1.4, -2, 2, A.CYANR, 0.6, True)
    m.b("grip", -1, 1, -1, 4, -1, 1, A.LEATH, 0.5, fn=tex_rows([(2, 3), (6, 7)], [(20, 10, 8), (50, 30, 24)]))
    m.b("guard", -4, 4, 4, 5.5, -1.6, 1.6, STEEL_LT, 0.5)
    m.sym("gtip", 4, 5, 4.3, 5.8, -1, 1, STEEL, 0.4)
    m.b("gem", -0.9, 0.9, 4.1, 5.4, -2, 2, A.CYANR, 0.6, True)
    m.b("blade", -1.5, 1.5, 5.5, 16.5, -0.5, 0.5, STEEL_LT, 0.5)
    m.b("ridge", -0.5, 0.5, 5.5, 17, -0.9, 0.9, STEEL_LT, 0.72)
    m.b("fuller", -0.25, 0.25, 7, 15, -0.96, 0.96, A.CYANR, 0.6, True)
    m.b("tip", -1, 1, 16.5, 18.2, -0.4, 0.4, STEEL_LT, 0.6)
    m.b("tip2", -0.5, 0.5, 18.2, 19.5, -0.3, 0.3, STEEL_LT, 0.75)
    return m


def pickaxe():
    m = Model("void_steel_pickaxe", True, ITEM_TEX, "item/model", 102)
    m.b("handle", -0.75, 0.75, -3, 15, -0.75, 0.75, A.LEATH, 0.5, fn=tex_rows([(8, 9), (20, 21), (30, 31)], [(20, 10, 8), (50, 30, 24)]))
    m.b("wrap_a", -1.1, 1.1, 10, 11, -1.1, 1.1, A.LEATH, 0.3)
    m.b("wrap_b", -1.1, 1.1, 3, 4, -1.1, 1.1, A.LEATH, 0.3)
    m.b("head", -2, 2, 14, 17.5, -1.3, 1.3, STEEL_LT, 0.5)
    m.sym("arm1", 2, 5, 13.6, 17, -1, 1, STEEL_LT, 0.5)
    m.sym("arm2", 5, 7.5, 12.3, 15.6, -0.8, 0.8, STEEL_LT, 0.55)
    m.sym("tipp", 7.5, 9.2, 10.6, 13.4, -0.55, 0.55, STEEL_LT, 0.7)
    m.b("gem", -1, 1, 17.5, 19, -1.6, 1.6, A.CYANR, 0.6, True)
    m.b("under", -1.6, 1.6, 13.5, 14, -1.35, 1.35, A.CYANR, 0.5, True)
    return m


def axe():
    m = Model("void_steel_axe", True, ITEM_TEX, "item/model", 103)
    m.b("handle", -0.75, 0.75, -3, 16, -0.75, 0.75, A.LEATH, 0.5, fn=tex_rows([(8, 9), (22, 23)], [(20, 10, 8), (50, 30, 24)]))
    m.b("cap", -1.1, 1.1, 16, 17, -1.1, 1.1, STEEL, 0.4)
    m.b("block", 0.75, 3, 11.5, 17, -1.5, 1.5, STEEL, 0.5)
    m.b("blade1", 3, 5.2, 10.8, 17.8, -0.7, 0.7, STEEL_LT, 0.5)
    m.b("blade2", 5.2, 7.2, 9.2, 19, -0.5, 0.5, STEEL_LT, 0.6)
    m.b("edge", 6.9, 7.4, 9.4, 18.8, -0.6, 0.6, A.CYANR, 0.6, True)
    m.b("spike", -3, -0.75, 13.8, 15.8, -0.9, 0.9, STEEL, 0.5)
    m.b("gem", 1, 2.6, 13, 15.5, -1.65, 1.65, A.CYANR, 0.6, True)
    return m


def shovel():
    m = Model("void_steel_shovel", True, ITEM_TEX, "item/model", 104)
    m.b("handle", -0.75, 0.75, -3, 11, -0.75, 0.75, A.LEATH, 0.5, fn=tex_rows([(6, 7), (18, 19)], [(20, 10, 8), (50, 30, 24)]))
    m.b("tgrip", -2.2, 2.2, -3, -1.8, -0.75, 0.75, A.LEATH, 0.4)
    m.b("collar", -1.3, 1.3, 11, 12.6, -1.3, 1.3, STEEL, 0.45)
    m.b("blade", -2.5, 2.5, 12.6, 18.6, -0.6, 0.6, STEEL_LT, 0.5)
    m.b("btip", -1.6, 1.6, 18.6, 20.2, -0.55, 0.55, STEEL_LT, 0.6)
    m.b("btip2", -0.7, 0.7, 20.2, 21, -0.5, 0.5, STEEL_LT, 0.75)
    m.b("ridge", -0.6, 0.6, 12.6, 20.4, -0.95, 0.95, STEEL_LT, 0.72)
    m.b("rune", -0.25, 0.25, 14, 18, -0.98, 0.98, A.CYANR, 0.6, True)
    return m


def hoe():
    m = Model("void_steel_hoe", True, ITEM_TEX, "item/model", 105)
    m.b("handle", -0.75, 0.75, -3, 16, -0.75, 0.75, A.LEATH, 0.5, fn=tex_rows([(8, 9), (22, 23)], [(20, 10, 8), (50, 30, 24)]))
    m.b("bar", 0.75, 6.5, 14.2, 16.8, -1, 1, STEEL_LT, 0.5)
    m.b("hook", 5, 6.5, 10.6, 14.2, -0.8, 0.8, STEEL_LT, 0.55)
    m.b("hook_tip", 5.4, 6.1, 9.6, 10.6, -0.6, 0.6, STEEL_LT, 0.75)
    m.b("counter", -2, -0.75, 14.6, 16.4, -0.9, 0.9, STEEL, 0.5)
    m.b("gem", 0.8, 2.4, 14.5, 16.5, -1.5, 1.5, A.CYANR, 0.6, True)
    return m


def rift_blade():
    m = Model("rift_blade", True, ITEM_TEX, "item/model", 106)
    m.b("pommel", -1.2, 1.2, -3, -1.4, -1.2, 1.2, A.PINK, 0.6, True)
    m.b("grip", -0.9, 0.9, -1.4, 4, -0.9, 0.9, DARKM, 0.5, fn=tex_rows([(2, 3), (7, 8)], [(60, 14, 70), (150, 40, 150)]))
    m.b("guard", -3.2, 3.2, 4, 5, -1.2, 1.2, STEEL, 0.5)
    m.sym("wing", 3.2, 4.4, 4.4, 6, -0.7, 0.7, STEEL, 0.5)
    m.b("core", -1, 1, 5, 6.4, -1.8, 1.8, A.PINK, 0.6, True)
    m.b("seg1", -1.3, 1.3, 5.2, 10.5, -0.5, 0.5, STEEL_LT, 0.55)
    m.b("seg2", -0.7, 1.9, 10.5, 15.5, -0.5, 0.5, STEEL_LT, 0.6)
    m.b("seg3", -0.2, 2.4, 15.5, 19.5, -0.5, 0.5, STEEL_LT, 0.65)
    m.b("btip", 0.3, 2.0, 19.5, 21, -0.35, 0.35, STEEL_LT, 0.8)
    m.b("e1", -1.5, -1.2, 5.4, 10.4, -0.62, 0.62, A.PINK, 0.6, True)
    m.b("e2", -0.9, -0.6, 10.5, 15.4, -0.62, 0.62, A.PINK, 0.6, True)
    m.b("e3", -0.4, -0.1, 15.5, 19.3, -0.62, 0.62, A.PINK, 0.6, True)
    return m


def reaper():
    m = Model("void_reaper", True, ITEM_TEX, "item/model", 107)
    m.b("shaft", -0.75, 0.75, -3, 17, -0.75, 0.75, DARKM, 0.5, fn=tex_rows([(10, 11), (26, 27)], [(60, 14, 70), (150, 40, 150)]))
    m.b("ring_a", -1.15, 1.15, 3, 3.8, -1.15, 1.15, A.GOLD, 0.5)
    m.b("ring_b", -1.15, 1.15, 9, 9.8, -1.15, 1.15, A.GOLD, 0.5)
    m.b("cap", -1.3, 1.3, 17, 18.2, -1.3, 1.3, STEEL, 0.45)
    m.b("gem", -1, 1, 14.2, 16, -1.3, 1.3, A.PINK, 0.6, True)
    m.b("ba", 0.2, 3.8, 17, 19.8, -0.6, 0.6, STEEL_LT, 0.55)
    m.b("bb", 3.8, 6.8, 15.8, 18.8, -0.6, 0.6, STEEL_LT, 0.55)
    m.b("bc", 6.5, 9.2, 13.2, 16.5, -0.6, 0.6, STEEL_LT, 0.6)
    m.b("bd", 8.5, 10.5, 10, 14, -0.5, 0.5, STEEL_LT, 0.7)
    m.b("ga", 0.4, 3.8, 16.6, 17.1, -0.7, 0.7, A.VIOL, 0.6, True)
    m.b("gb", 3.8, 6.8, 15.4, 15.9, -0.7, 0.7, A.VIOL, 0.6, True)
    m.b("gc", 6.5, 9.0, 12.8, 13.3, -0.7, 0.7, A.VIOL, 0.6, True)
    m.b("gd", 8.5, 8.9, 10.2, 12.7, -0.6, 0.6, A.VIOL, 0.6, True)
    m.b("spike", -2.2, -0.2, 16.8, 18, -0.5, 0.5, STEEL, 0.5)
    return m


def piercer():
    m = Model("voidpiercer", True, ITEM_TEX, "item/model", 108)
    m.b("shaft", -0.7, 0.7, -3, 12, -0.7, 0.7, A.LEATH, 0.5, fn=tex_rows([(6, 7), (18, 19), (28, 29)], [(20, 10, 8), (50, 30, 24)]))
    m.b("band_a", -1.1, 1.1, 0, 0.8, -1.1, 1.1, A.GOLD, 0.5)
    m.b("band_b", -1.1, 1.1, 5, 5.8, -1.1, 1.1, A.GOLD, 0.5)
    m.b("butt", -1.1, 1.1, -3.8, -3, -1.1, 1.1, STEEL, 0.4)
    m.b("socket", -1.4, 1.4, 12, 13.4, -1.4, 1.4, A.GOLD, 0.55)
    m.b("sgem", -0.9, 0.9, 12.2, 13.2, -1.5, 1.5, A.CYANR, 0.6, True)
    m.b("h1", -2, 2, 13.4, 15.6, -0.55, 0.55, STEEL_LT, 0.55)
    m.b("h2", -1.4, 1.4, 15.6, 17.8, -0.5, 0.5, STEEL_LT, 0.6)
    m.b("h3", -0.8, 0.8, 17.8, 19.6, -0.45, 0.45, STEEL_LT, 0.7)
    m.b("h4", -0.35, 0.35, 19.6, 20.8, -0.35, 0.35, STEEL_LT, 0.85)
    m.sym("fin", 2, 3.6, 13.4, 14.8, -0.4, 0.4, STEEL, 0.5)
    m.sym("fint", 3.6, 4.4, 14.2, 16, -0.3, 0.3, STEEL_LT, 0.7)
    m.b("edge", -0.3, 0.3, 13.6, 19.8, -0.62, 0.62, A.CYANR, 0.6, True)
    return m


def staff():
    m = Model("gravity_staff", True, ITEM_TEX, "item/model", 109)
    m.b("shaft", -0.8, 0.8, -3, 13, -0.8, 0.8, DARKM, 0.5, fn=tex_rows([(8, 9), (20, 21)], [(60, 14, 70), (150, 40, 150)]))
    m.b("ring_a", -1.2, 1.2, 2, 2.8, -1.2, 1.2, A.GOLD, 0.5)
    m.b("ring_b", -1.2, 1.2, 8, 8.8, -1.2, 1.2, A.GOLD, 0.5)
    m.b("base", -1.5, 1.5, 13, 14, -1.5, 1.5, STEEL, 0.45)
    m.b("prong_a", 1.4, 2.2, 13, 19, 1.4, 2.2, STEEL_LT, 0.5)
    m.b("prong_b", -2.2, -1.4, 13, 19, 1.4, 2.2, STEEL_LT, 0.5, share="prong_a")
    m.b("prong_c", 1.4, 2.2, 13, 19, -2.2, -1.4, STEEL_LT, 0.5, share="prong_a")
    m.b("prong_d", -2.2, -1.4, 13, 19, -2.2, -1.4, STEEL_LT, 0.5, share="prong_a")
    m.b("orb", -1.5, 1.5, 14.5, 18, -1.5, 1.5, A.CYANR, 0.5, True)
    m.b("orb_core", -0.8, 0.8, 15.2, 17.3, -0.8, 0.8, A.CYANR, 0.95, True)
    m.b("ring_n", -2.8, 2.8, 16, 16.6, -2.8, -2.4, A.GOLD, 0.55)
    m.b("ring_s", -2.8, 2.8, 16, 16.6, 2.4, 2.8, A.GOLD, 0.55, share="ring_n")
    m.b("ring_w", -2.8, -2.4, 16, 16.6, -2.4, 2.4, A.GOLD, 0.55)
    m.b("ring_e", 2.4, 2.8, 16, 16.6, -2.4, 2.4, A.GOLD, 0.55, share="ring_w")
    m.b("top", -0.5, 0.5, 19, 21, -0.5, 0.5, STEEL_LT, 0.7)
    return m


# ------------------------------------------------------------------ vat pham (khong cam kieu kiem)
def shard():
    m = Model("void_shard", False, ITEM_TEX, "item/model", 110)
    m.b("rock", -3.5, 3.5, 1, 2.6, -3, 3, [(20, 18, 28), (46, 42, 60), (80, 74, 100), (120, 112, 140)], 0.45)
    m.b("main", -1.5, 1.5, 2.6, 11, -1.5, 1.5, A.VIOL, 0.5, True)
    m.b("tip", -0.8, 0.8, 11, 13.5, -0.8, 0.8, A.VIOL, 0.8, True)
    m.b("side1", 2, 4, 2.6, 8.5, -1, 1, A.VIOL, 0.45, True, rot=("z", 22.5))
    m.b("side2", -4.2, -2.2, 2.6, 7.5, -1, 1, A.VIOL, 0.55, True, rot=("z", -22.5))
    m.b("side3", -1, 1, 2.6, 7, 2, 4, A.VIOL, 0.6, True, rot=("x", 22.5))
    return m


def ingot():
    m = Model("void_steel_ingot", False, ITEM_TEX, "item/model", 111)
    m.b("bot", -5, 5, 5, 7.2, -2.8, 2.8, STEEL, 0.5)
    m.b("top", -4, 4, 7.2, 9.2, -2.0, 2.0, STEEL_LT, 0.55)
    m.b("rune_a", -2.6, 2.6, 9.2, 9.6, -0.35, 0.35, A.CYANR, 0.6, True)
    m.b("rune_b", -0.35, 0.35, 9.2, 9.6, -1.4, 1.4, A.CYANR, 0.6, True)
    return m


def silk():
    m = Model("phase_silk", False, ITEM_TEX, "item/model", 112)
    m.b("core", -1, 1, 3, 13, -1, 1, DARKM, 0.5)
    m.b("fl_top", -3.5, 3.5, 11.8, 13, -3.5, 3.5, A.GOLD, 0.5)
    m.b("fl_bot", -3.5, 3.5, 3, 4.2, -3.5, 3.5, A.GOLD, 0.45)
    m.b("wrap", -2.6, 2.6, 4.2, 11.8, -2.6, 2.6, SILK_R, 0.55,
        fn=tex_rows([(3, 3), (7, 7), (11, 11), (15, 15), (19, 19)], [(220, 120, 240), (255, 200, 255)]))
    m.b("sparkle", -2.75, 2.75, 7.4, 8.2, -2.75, 2.75, A.PINK, 0.6, True)
    return m


def core():
    m = Model("rift_core", False, ITEM_TEX, "item/model", 113)
    m.b("cube_a", -2.4, 2.4, 5.6, 10.4, -2.4, 2.4, A.PINK, 0.6, True, rot=("y", 45))
    m.b("cube_b", -1.5, 1.5, 6.5, 9.5, -1.5, 1.5, A.PINK, 0.98, True, rot=("x", 45))
    o = [8, 8, 8]
    m.b("ring_n", -4.6, 4.6, 7.6, 8.4, -4.6, -4.0, A.GOLD, 0.55, rot=("y", 45, o))
    m.b("ring_s", -4.6, 4.6, 7.6, 8.4, 4.0, 4.6, A.GOLD, 0.55, rot=("y", 45, o), share="ring_n")
    m.b("ring_w", -4.6, -4.0, 7.6, 8.4, -4.0, 4.0, A.GOLD, 0.55, rot=("y", 45, o))
    m.b("ring_e", 4.0, 4.6, 7.6, 8.4, -4.0, 4.0, A.GOLD, 0.55, rot=("y", 45, o), share="ring_w")
    return m


def apple():
    m = Model("void_apple", False, ITEM_TEX, "item/model", 114)
    m.b("low", -3.5, 3.5, 2, 8, -3, 3, APPLE, 0.5)
    m.b("mid", -4, 4, 3, 7, -3.5, 3.5, APPLE, 0.55)
    m.b("top", -3, 3, 8, 10, -2.6, 2.6, APPLE, 0.6)
    m.b("stem", -0.4, 0.4, 10, 12.5, -0.4, 0.4, A.LEATH, 0.45, rot=("z", 15))
    m.b("leaf", 0.8, 3.4, 11, 11.8, -1.0, 1.0, GREEN_R, 0.55)
    m.b("spot_a", -0.6, 0.6, 4.5, 6.2, 3.5, 3.8, A.CYANR, 0.7, True)
    m.b("spot_b", 3.5, 3.8, 5, 6.5, -0.6, 0.6, A.CYANR, 0.7, True)
    return m


# ------------------------------------------------------------------ den 3D
def lantern():
    m = Model("rift_lantern", False, BLOCK_TEX, "block/model", 120)
    PL = [(14, 8, 30), (40, 26, 80), (80, 56, 140), (130, 106, 200)]
    m.b("base", -5, 5, 0, 1.5, -5, 5, PL, 0.45)
    m.b("top", -5, 5, 14.5, 16, -5, 5, PL, 0.5)
    for i, (sx, sz) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1))):
        x0, x1 = (3.5, 5.0) if sx > 0 else (-5.0, -3.5)
        z0, z1 = (3.5, 5.0) if sz > 0 else (-5.0, -3.5)
        m.b("post_%d" % i, x0, x1, 1.5, 14.5, z0, z1, PL, 0.5, share="post_0" if i else None)
    m.b("cap", -1, 1, 16, 18, -1, 1, PL, 0.6)
    m.b("core_a", -2.5, 2.5, 5.5, 10.5, -2.5, 2.5, A.PINK, 0.7, True, rot=("y", 45))
    m.b("core_b", -1.7, 1.7, 6.3, 9.7, -1.7, 1.7, A.PINK, 0.98, True, rot=("x", 45))
    m.b("glow_ring", -3.6, 3.6, 7.7, 8.3, -3.6, 3.6, A.VIOL, 0.7, True, rot=("y", 22.5))
    return m


def ore_crystals():
    """Quang co tinh the 3D moc ra khoi cac mat khoi (hien khi quang lo thien trong hang)."""
    img = Image.new("RGBA", (16, 16))
    rng = random.Random(5)
    for y in range(16):
        for x in range(16):
            t = 0.25 + 0.6 * (1 - y / 15.0) + 0.12 * (0.5 - abs(x - 7.5) / 8) + rng.uniform(-0.05, 0.05)
            img.putpixel((x, y), A.ramp([(60, 30, 140), (120, 70, 225), (180, 140, 255), (240, 225, 255)], t))
    img.save(os.path.join(BLOCK_TEX, "void_crystal.png"))

    def cube_face(d):
        return {"uv": [0, 0, 16, 16], "texture": "#base", "cullface": d}

    def crystal(face, u0, v0, w, d, ln, tilt=None):
        n0, n1 = 0, ln
        if face == "up":
            fr, to = [u0, 16 + n0, v0], [u0 + w, 16 + n1, v0 + d]
        elif face == "down":
            fr, to = [u0, -n1, v0], [u0 + w, -n0, v0 + d]
        elif face == "north":
            fr, to = [u0, v0, -n1], [u0 + w, v0 + d, -n0]
        elif face == "south":
            fr, to = [u0, v0, 16 + n0], [u0 + w, v0 + d, 16 + n1]
        elif face == "west":
            fr, to = [-n1, u0, v0], [-n0, u0 + w, v0 + d]
        else:
            fr, to = [16 + n0, u0, v0], [16 + n1, u0 + w, v0 + d]
        el = {"from": fr, "to": to, "shade": False, "neoforge_data": {"block_light": 12, "sky_light": 12},
              "faces": {k: {"uv": [0, 0, 16, 16], "texture": "#crystal"} for k in ("north", "south", "east", "west", "up", "down")}}
        if tilt:
            el["rotation"] = {"origin": [(fr[0] + to[0]) / 2, (fr[1] + to[1]) / 2, (fr[2] + to[2]) / 2], "axis": tilt[0], "angle": tilt[1]}
        return el

    for ore, base in (("void_crystal_ore", "block/void_crystal_ore"), ("deepslate_void_crystal_ore", "block/deepslate_void_crystal_ore")):
        els = [{"from": [0, 0, 0], "to": [16, 16, 16], "faces": {d: cube_face(d) for d in ("north", "south", "east", "west", "up", "down")}}]
        for face in ("up", "down", "north", "south", "west", "east"):
            els.append(crystal(face, 3, 4, 2, 2, 3.2, ("x", 22.5)))
            els.append(crystal(face, 10, 9, 2, 2, 2.2, ("z", -22.5)))
        obj = {"parent": "minecraft:block/block", "textures": {"base": "voidrealm:" + base, "crystal": "voidrealm:block/model/void_crystal",
                                                               "particle": "voidrealm:" + base}, "elements": els}
        with open(os.path.join(ROOT, "models", "block", ore + ".json"), "w") as f:
            json.dump(obj, f, indent=1)


if __name__ == "__main__":
    total = 0
    for fn in (sword, pickaxe, axe, shovel, hoe, rift_blade, reaper, piercer, staff, shard, ingot, silk, core, apple):
        m = fn()
        n = m.write_item()
        total += n
        print("%-22s %3d phan" % (m.name, n))
    n = lantern().write_block("voidrealm:block/rift_lantern")
    print("%-22s %3d phan" % ("rift_lantern", n))
    ore_crystals()
    print("Xong model 3D")
