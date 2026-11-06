#!/usr/bin/env python3
"""Magitech: texture + model Java cho Void Wisp, Void Stalker Bird; model 3D item/khoi moi; data (lang, recipe, loot, spawn).
Chay SAU gen_data.py, gen_models.py, gen_armor.py:   python3 tools/gen_magitech.py
"""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image  # noqa: E402
import gen_art as A  # noqa: E402
from gen_art import hash2, vnoise, ramp  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RES = os.path.join(ROOT, "src", "main", "resources")
ASSETS = os.path.join(RES, "assets", "voidrealm")
DATA = os.path.join(RES, "data", "voidrealm")
JAVA = os.path.join(ROOT, "src", "main", "java", "com", "voidrealm", "mod", "client", "MagitechModels.java")
ENT_TEX = os.path.join(ASSETS, "textures", "entity")
os.makedirs(ENT_TEX, exist_ok=True)

NS = "voidrealm"
CYAN = [(16, 90, 110), (40, 180, 200), (120, 240, 245), (225, 255, 255)]
VIOL = [(20, 10, 50), (50, 26, 110), (96, 56, 180), (160, 120, 245)]
NIGHT = [(10, 6, 26), (26, 16, 58), (52, 32, 104), (96, 68, 168)]
LAV = [(60, 40, 110), (120, 90, 190), (180, 150, 235), (232, 218, 255)]
GOLD = [(120, 80, 16), (200, 150, 40), (250, 210, 90), (255, 240, 170)]
WHITE = [(90, 150, 200), (150, 220, 250), (220, 250, 255), (255, 255, 255)]


# ======================================================================= packer + painter
class Atlas:
    def __init__(self, w, h, seed):
        self.w, self.h, self.seed = w, h, seed
        self.img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.x = self.y = self.row_h = 0
        self.boxes = {}

    def alloc(self, name, W, H, D):
        bw, bh = 2 * (W + D), D + H
        if self.x + bw > self.w:
            self.x, self.y, self.row_h = 0, self.y + self.row_h, 0
        if self.y + bh > self.h:
            raise RuntimeError("het cho: " + name)
        u, v = self.x, self.y
        self.x += bw
        self.row_h = max(self.row_h, bh)
        self.boxes[name] = (u, v, W, H, D)
        return u, v

    def faces(self, name):
        u, v, W, H, D = self.boxes[name]
        return {"top": (u + D, v, W, D), "bottom": (u + D + W, v, W, D), "right": (u, v + D, D, H),
                "front": (u + D, v + D, W, H), "left": (u + D + W, v + D, D, H), "back": (u + 2 * D + W, v + D, W, H)}

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.img.putpixel((x, y), (c[0], c[1], c[2], 255))

    def paint(self, name, cols, base=0.5, grain=0.16, scale=2.2, only=None):
        for fname, (fx, fy, fw, fh) in self.faces(name).items():
            if only and fname not in only:
                continue
            shade = {"top": 0.12, "bottom": -0.16, "front": 0.04, "back": -0.04, "left": -0.02, "right": 0.0}[fname]
            for j in range(fh):
                for i in range(fw):
                    n = vnoise(fx + i, fy + j, scale, self.seed) - 0.5
                    n += (hash2(fx + i, fy + j, self.seed + 3) - 0.5) * 0.3
                    t = base + shade + n * grain * 2
                    if i == 0 or j == 0:
                        t += 0.07
                    if i == fw - 1 or j == fh - 1:
                        t -= 0.09
                    self.px(fx + i, fy + j, ramp(cols, max(0.0, min(1.0, t))))

    def f(self, name, face, x, y, c):
        fx, fy, fw, fh = self.faces(name)[face]
        if 0 <= x < fw and 0 <= y < fh:
            self.px(fx + x, fy + y, c)

    def band(self, name, face_list, y0, y1, c):
        for face in face_list:
            fx, fy, fw, fh = self.faces(name)[face]
            for y in range(y0, min(y1, fh - 1) + 1):
                for x in range(fw):
                    self.px(fx + x, fy + y, c)

    def save(self, path):
        self.img.save(path)


def java_part(parent, name, u, v, box, pivot, rot=(0, 0, 0)):
    x, y, z, w, h, d = box
    px, py, pz = pivot
    pose = "PartPose.offset(%sF, %sF, %sF)" % (px, py, pz)
    if rot != (0, 0, 0):
        pose = "PartPose.offsetAndRotation(%sF, %sF, %sF, %sF, %sF, %sF)" % (px, py, pz, rot[0], rot[1], rot[2])
    return '        PartDefinition %s = %s.addOrReplaceChild("%s", CubeListBuilder.create().texOffs(%d, %d).addBox(%sF, %sF, %sF, %sF, %sF, %sF), %s);' % (
        name, parent, name, u, v, x, y, z, w, h, d, pose)


# ======================================================================= VOID WISP
def build_wisp():
    at = Atlas(64, 64, 71)
    parts = [  # name, parent, W,H,D, origin, pivot, rot
        ("core", "root", 6, 6, 6, (-3, -3, -3), (0, 20, 0), (0, 0, 0)),
        ("shell", "core", 8, 8, 8, (-4, -4, -4), (0, 0, 0), (0, 0, 0)),
        ("orbit", "root", 1, 1, 1, (0, 0, 0), (0, 20, 0), (0, 0, 0)),
        ("o1", "orbit", 2, 2, 2, (-1, -1, -1), (7, 0, 0), (0, 0, 0)),
        ("o2", "orbit", 2, 2, 2, (-1, -1, -1), (-7, 0, 0), (0, 0, 0)),
        ("o3", "orbit", 2, 2, 2, (-1, -1, -1), (0, -3, 7), (0, 0, 0)),
        ("o4", "orbit", 2, 2, 2, (-1, -1, -1), (0, 3, -7), (0, 0, 0)),
        ("tail", "root", 2, 2, 4, (-1, -1, 0), (0, 21, 3), (0.5, 0, 0)),
    ]
    for (n, p, W, H, D, o, pv, r) in parts:
        at.alloc(n, W, H, D)
    at.paint("core", WHITE, 0.62, 0.08)
    at.paint("shell", CYAN, 0.58, 0.12)
    # lop vo: chi giu vien (mau trong suot khi nam giua) -> xoa mat giua cho do cham
    for fname, (fx, fy, fw, fh) in at.faces("shell").items():
        for j in range(1, fh - 1):
            for i in range(1, fw - 1):
                if (i + j) % 2 == 0:
                    at.img.putpixel((fx + i, fy + j), (0, 0, 0, 0))
    for n in ("o1", "o2", "o3", "o4"):
        at.paint(n, VIOL, 0.7, 0.1)
        for face in ("front", "back", "left", "right", "top"):
            at.f(n, face, 0, 0, (230, 200, 255))
    at.paint("tail", CYAN, 0.5, 0.15)
    # mat tren mat truoc loi
    at.f("core", "front", 1, 2, (10, 20, 60))
    at.f("core", "front", 2, 2, (10, 20, 60))
    at.f("core", "front", 3, 2, (10, 20, 60))
    at.f("core", "front", 4, 2, (10, 20, 60))
    at.f("core", "front", 1, 3, (10, 20, 60))
    at.f("core", "front", 4, 3, (10, 20, 60))
    for x in (2, 3):
        at.f("core", "front", x, 3, (160, 255, 255))
    at.save(os.path.join(ENT_TEX, "void_wisp.png"))
    lines = ["    public static LayerDefinition wisp() {",
             "        MeshDefinition mesh = new MeshDefinition();",
             "        PartDefinition root = mesh.getRoot();"]
    for (n, p, W, H, D, o, pv, r) in parts:
        u, v = at.boxes[n][0], at.boxes[n][1]
        lines.append(java_part(p, n, u, v, o + (W, H, D), pv, r))
    lines += ["        return LayerDefinition.create(mesh, 64, 64);", "    }"]
    return "\n".join(lines)


# ======================================================================= VOID STALKER BIRD
def build_bird():
    at = Atlas(64, 64, 83)
    P = [  # name, parent, W,H,D, origin, pivot, rot
        ("body", "root", 6, 6, 10, (-3, -3, -5), (0, 16, 0), (0, 0, 0)),
        ("chest", "body", 5, 4, 3, (-2.5, -1.5, -7.5), (0, 0, 0), (0, 0, 0)),
        ("head", "body", 4, 4, 4, (-2, -2, -3), (0, -3.5, -5.5), (0, 0, 0)),
        ("beak_up", "head", 2, 1, 3, (-1, -0.6, -6), (0, 0, 0), (0, 0, 0)),
        ("beak_low", "head", 2, 1, 2, (-1, 0.4, -5), (0, 0, 0), (0, 0, 0)),
        ("crest", "head", 1, 3, 4, (-0.5, -4.6, -1), (0, 0, 0), (0.25, 0, 0)),
        ("wing_r", "body", 10, 1, 6, (0, -0.5, -3), (3, -1.5, -1), (0, 0, 0)),
        ("tip_r", "wing_r", 8, 1, 5, (0, -0.4, -2.5), (10, 0, 0), (0, 0, 0)),
        ("wing_l", "body", 10, 1, 6, (-10, -0.5, -3), (-3, -1.5, -1), (0, 0, 0)),
        ("tip_l", "wing_l", 8, 1, 5, (-8, -0.4, -2.5), (-10, 0, 0), (0, 0, 0)),
        ("tail_c", "body", 3, 1, 9, (-1.5, -0.5, 0), (0, 0.5, 5), (0.12, 0, 0)),
        ("tail_l", "body", 3, 1, 8, (-1.5, -0.5, 0), (0, 0.5, 5), (0.12, -0.35, 0)),
        ("tail_r", "body", 3, 1, 8, (-1.5, -0.5, 0), (0, 0.5, 5), (0.12, 0.35, 0)),
        ("leg_r", "body", 1, 4, 1, (-0.5, 0, -0.5), (1.8, 3, 1), (0, 0, 0)),
        ("foot_r", "leg_r", 3, 1, 3, (-1.5, 0, -2), (0, 4, 0), (0, 0, 0)),
        ("leg_l", "body", 1, 4, 1, (-0.5, 0, -0.5), (-1.8, 3, 1), (0, 0, 0)),
        ("foot_l", "leg_l", 3, 1, 3, (-1.5, 0, -2), (0, 4, 0), (0, 0, 0)),
    ]
    for (n, p, W, H, D, o, pv, r) in P:
        at.alloc(n, int(W), int(H), int(D))

    at.paint("body", NIGHT, 0.5, 0.2, 1.8)
    at.paint("chest", LAV, 0.5, 0.15)
    # nguc: vet long lang chevron
    for face in ("front",):
        for j in range(4):
            for i in range(5):
                if (i + j) % 2 == 0:
                    at.f("chest", face, i, j, ramp(LAV, 0.35))
    # than: vet long doc theo lung
    for j in range(0, 10, 2):
        for i in range(0, 6):
            at.f("body", "top", i, j, ramp(VIOL, 0.55 + 0.1 * ((i + j) % 3)))
    for face in ("right", "left"):
        for j in range(0, 6):
            for i in range(0, 10):
                if i % 3 == 1:
                    at.f("body", face, i, j, ramp(VIOL, 0.5))
    # dau
    at.paint("head", NIGHT, 0.52, 0.18)
    for face in ("right", "left"):
        at.f("head", face, 2, 1, (255, 255, 255))
        at.f("head", face, 2, 2, CYAN[2])
        at.f("head", face, 3, 1, CYAN[3])
        at.f("head", face, 3, 2, CYAN[1])
    at.paint("beak_up", GOLD, 0.62, 0.08)
    at.paint("beak_low", GOLD, 0.4, 0.08)
    at.paint("crest", CYAN, 0.6, 0.12)
    for j in range(0, 3):
        at.f("crest", "right", j + 1, 1, CYAN[3])
        at.f("crest", "left", j + 1, 2, CYAN[3])
    # canh: long vu xep hang + dau canh sang xanh
    for name in ("wing_r", "wing_l"):
        at.paint(name, VIOL, 0.5, 0.16, 1.4)
        for face in ("top", "bottom"):
            fx, fy, fw, fh = at.faces(name)[face]
            for i in range(fw):
                for j in range(fh):
                    k = (i // 2 + j) % 2
                    at.px(fx + i, fy + j, ramp(VIOL if face == "top" else NIGHT, 0.46 + 0.14 * k + 0.12 * (j / max(1, fh - 1)) * (1 if face == "top" else -1)))
            # vien trong long (cuoi canh sang)
            for j in range(fh):
                at.px(fx + (fw - 1 if name == "wing_r" else 0), fy + j, CYAN[1])
    for name in ("tip_r", "tip_l"):
        at.paint(name, VIOL, 0.46, 0.16, 1.4)
        for face in ("top", "bottom"):
            fx, fy, fw, fh = at.faces(name)[face]
            for i in range(fw):
                for j in range(fh):
                    base = 0.5 + 0.18 * ((i // 2 + j) % 2)
                    tipi = (fw - 1 - i) if name == "tip_r" else i
                    c = ramp(CYAN, 0.3 + 0.22 * (3 - min(3, tipi))) if tipi < 3 else ramp(VIOL if face == "top" else NIGHT, base)
                    at.px(fx + i, fy + j, c)
    # duoi: 3 chiec long, dau long sang
    for name in ("tail_c", "tail_l", "tail_r"):
        at.paint(name, VIOL, 0.45, 0.14)
        for face in ("top", "bottom"):
            fx, fy, fw, fh = at.faces(name)[face]
            for j in range(fh):
                for i in range(fw):
                    if j >= fh - 3:
                        at.px(fx + i, fy + j, ramp(CYAN, 0.35 + 0.2 * (j - (fh - 3))))
                    elif i == 1:
                        at.px(fx + i, fy + j, ramp(NIGHT, 0.7))
    for name in ("leg_r", "leg_l"):
        at.paint(name, GOLD, 0.35, 0.1)
    for name in ("foot_r", "foot_l"):
        at.paint(name, GOLD, 0.5, 0.1)
    at.save(os.path.join(ENT_TEX, "void_stalker_bird.png"))
    lines = ["    public static LayerDefinition bird() {",
             "        MeshDefinition mesh = new MeshDefinition();",
             "        PartDefinition root = mesh.getRoot();"]
    for (n, p, W, H, D, o, pv, r) in P:
        u, v = at.boxes[n][0], at.boxes[n][1]
        lines.append(java_part(p, n, u, v, tuple(o) + (W, H, D), pv, r))
    lines += ["        return LayerDefinition.create(mesh, 64, 64);", "    }"]
    return "\n".join(lines)


def write_java(wisp, bird):
    src = """package com.voidrealm.mod.client;

import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.client.model.geom.PartPose;

/** Tu dong sinh boi tools/gen_magitech.py - KHONG sua tay. */
public final class MagitechModels {
%s

%s

    private MagitechModels() {
    }
}
""" % (wisp, bird)
    with open(JAVA, "w", encoding="utf-8") as f:
        f.write(src)



# ======================================================================= ITEM / BLOCK 3D
import gen_models as GM  # noqa: E402

BLACKM = [(2, 0, 8), (12, 4, 30), (30, 12, 66), (60, 30, 120)]
ROPE = [(70, 44, 24), (130, 92, 52), (190, 150, 96), (230, 200, 150)]
GLASS = [(70, 120, 150), (130, 190, 215), (190, 235, 250), (240, 255, 255)]
CAKE = [(110, 60, 20), (190, 120, 50), (235, 180, 90), (255, 225, 150)]
CREAM = [(120, 90, 190), (170, 140, 235), (215, 195, 255), (245, 235, 255)]
BANANA = [(150, 110, 20), (225, 185, 50), (255, 228, 100), (255, 248, 190)]
BRICK = [(14, 8, 30), (36, 24, 70), (70, 52, 120), (110, 90, 170)]
WOOD = [(60, 36, 16), (110, 70, 34), (160, 110, 60), (200, 150, 90)]
ORANGE = GM.ORANGE_R


def warp_rod():
    m = GM.Model("warp_rod", True, GM.ITEM_TEX, "item/model", 201)
    m.b("shaft", -0.75, 0.75, -3, 12, -0.75, 0.75, GM.DARKM, 0.5,
        fn=GM.tex_rows([(8, 9), (20, 21)], [(60, 14, 70), (150, 40, 150)]))
    m.b("ring_a", -1.2, 1.2, 1.5, 2.4, -1.2, 1.2, A.GOLD, 0.5)
    m.b("ring_b", -1.2, 1.2, 7.5, 8.4, -1.2, 1.2, A.GOLD, 0.5)
    m.b("pommel", -1.3, 1.3, -4, -3, -1.3, 1.3, GM.STEEL, 0.45)
    m.b("cup", -2.4, 2.4, 12, 13.2, -2.4, 2.4, A.GOLD, 0.55)
    m.sym("claw_lo", 2.0, 3.0, 13, 16.5, -0.7, 0.7, GM.STEEL_LT, 0.5)
    m.sym("claw_hi", 1.3, 2.3, 16.5, 19.5, -0.55, 0.55, GM.STEEL_LT, 0.62)
    m.sym("claw_tip", 0.8, 1.6, 19.5, 20.8, -0.4, 0.4, A.CYANR, 0.8, True)
    m.b("hole_a", -2.2, 2.2, 14, 18, -2.2, 2.2, BLACKM, 0.35)
    m.b("hole_b", -1.4, 1.4, 14.8, 18.8, -1.4, 1.4, BLACKM, 0.18)
    m.b("disc_n", -4.2, 4.2, 15.7, 16.3, -4.2, -3.2, ORANGE, 0.6, True)
    m.b("disc_s", -4.2, 4.2, 15.7, 16.3, 3.2, 4.2, ORANGE, 0.6, True, share="disc_n")
    m.b("disc_w", -4.2, -3.2, 15.7, 16.3, -3.2, 3.2, A.PINK, 0.6, True)
    m.b("disc_e", 3.2, 4.2, 15.7, 16.3, -3.2, 3.2, A.PINK, 0.6, True, share="disc_w")
    m.b("disc_in", -3.2, 3.2, 15.9, 16.1, -3.2, 3.2, A.VIOL, 0.7, True)
    return m


def eye():
    m = GM.Model("eye_of_the_void", False, GM.ITEM_TEX, "item/model", 202)
    m.b("eA", -4, 4, 4, 12, -3, 3, CREAM, 0.6)
    m.b("eB", -3, 3, 3, 13, -3, 3, CREAM, 0.55)
    m.b("eC", -3, 3, 4, 12, -4, 4, CREAM, 0.58)
    for sgn, nm in ((-1, "n"), (1, "s")):
        z0, z1 = (-4.5, -4.0) if sgn < 0 else (4.0, 4.5)
        m.b("iris_" + nm, -2.4, 2.4, 5.6, 10.4, z0 - 0.0, z1, A.CYANR, 0.65, True)
        m.b("pupil_" + nm, -0.6, 0.6, 5.9, 10.1, z0 - 0.05 if sgn < 0 else z0 + 0.05, z1 + 0.05 if sgn < 0 else z1 + 0.05, BLACKM, 0.1)
        m.b("glint_" + nm, 0.9, 1.7, 8.7, 9.5, z0 - 0.1 if sgn < 0 else z0 + 0.1, z1 + 0.1 if sgn < 0 else z1 + 0.1, GM.STEEL_LT, 0.95, True)
    m.b("rim_top", -3.4, 3.4, 12, 13, -3.4, 3.4, A.GOLD, 0.55)
    m.b("rim_bot", -3.4, 3.4, 3, 4, -3.4, 3.4, A.GOLD, 0.45)
    m.sym("fin", 4, 6.5, 6.2, 9.8, -0.6, 0.6, GM.STEEL, 0.5)
    m.sym("fin_tip", 6.5, 8.6, 7, 9, -0.45, 0.45, A.VIOL, 0.65, True)
    m.b("crown", -0.8, 0.8, 13, 15, -0.8, 0.8, A.VIOL, 0.7, True)
    m.b("vein_a", -4.1, 4.1, 7.6, 8.4, -3.1, 3.1, A.VIOL, 0.6, True)
    return m


def tether():
    m = GM.Model("void_tether", True, GM.ITEM_TEX, "item/model", 203)
    m.b("grip", -0.9, 0.9, -3, 5, -0.9, 0.9, A.LEATH, 0.5,
        fn=GM.tex_rows([(4, 5), (10, 11)], [(20, 10, 8), (50, 30, 24)]))
    m.b("pommel", -1.4, 1.4, -4.2, -3, -1.4, 1.4, A.GOLD, 0.5)
    m.b("reel", -2.2, 2.2, 5, 9.5, -1.6, 1.6, A.GOLD, 0.5)
    m.b("coil_a", -2.8, 2.8, 5.8, 6.8, -2.1, 2.1, ROPE, 0.5)
    m.b("coil_b", -2.8, 2.8, 7.4, 8.4, -2.1, 2.1, ROPE, 0.55)
    m.b("hub", -1, 1, 6, 8.6, -2.3, 2.3, A.CYANR, 0.6, True)
    m.b("barrel", -1.1, 1.1, 9.5, 13, -1.1, 1.1, GM.STEEL, 0.5)
    m.b("muzzle", -1.5, 1.5, 13, 14.2, -1.5, 1.5, A.GOLD, 0.5)
    m.b("spike", -0.7, 0.7, 14.2, 17.5, -0.7, 0.7, GM.STEEL_LT, 0.65)
    m.b("spike_tip", -0.35, 0.35, 17.5, 19.3, -0.35, 0.35, A.CYANR, 0.8, True)
    m.sym("prong_lo", 1.5, 3.2, 14.2, 15.4, -0.5, 0.5, GM.STEEL_LT, 0.55)
    m.sym("prong_up", 2.6, 3.6, 15.4, 18, -0.45, 0.45, GM.STEEL_LT, 0.65)
    m.sym("prong_tip", 3.0, 3.8, 18, 19.2, -0.35, 0.35, A.CYANR, 0.8, True)
    m.b("loop", 1.1, 2.6, 8.4, 9.4, -0.6, 0.6, ROPE, 0.6)
    return m


def wisp_core():
    m = GM.Model("wisp_core", False, GM.ITEM_TEX, "item/model", 204)
    m.b("cap", -1.2, 1.2, 13, 14.5, -1.2, 1.2, A.GOLD, 0.55)
    m.b("ring_top", -3.2, 3.2, 11.6, 12.6, -3.2, 3.2, A.GOLD, 0.5)
    m.b("ring_bot", -3.2, 3.2, 3.6, 4.6, -3.2, 3.2, A.GOLD, 0.45)
    m.b("tipb", -1, 1, 2, 3.6, -1, 1, GM.STEEL, 0.5)
    for i, (x0, x1, z0, z1) in enumerate(((2.6, 3.4, 2.6, 3.4), (-3.4, -2.6, 2.6, 3.4), (2.6, 3.4, -3.4, -2.6), (-3.4, -2.6, -3.4, -2.6))):
        m.b("post_%d" % i, x0, x1, 4.6, 11.6, z0, z1, A.GOLD, 0.5, share="post_0" if i else None)
    m.b("orb_a", -2.4, 2.4, 5.6, 10.4, -2.4, 2.4, GM.WHITE_R if hasattr(GM, "WHITE_R") else WHITE, 0.8, True, rot=("y", 45))
    m.b("orb_b", -2.0, 2.0, 6.0, 10.0, -2.0, 2.0, WHITE, 0.95, True, rot=("x", 45))
    m.b("sh_a", 4.2, 5.2, 8.4, 10.2, -0.5, 0.5, A.CYANR, 0.7, True)
    m.b("sh_b", -5.2, -4.2, 5.6, 7.4, -0.5, 0.5, A.CYANR, 0.7, True)
    return m


def flux_vial():
    m = GM.Model("void_flux", False, GM.ITEM_TEX, "item/model", 205)
    m.b("cork", -1.3, 1.3, 12.4, 14, -1.3, 1.3, WOOD, 0.5)
    m.b("neck", -1.6, 1.6, 10, 12.4, -1.6, 1.6, GLASS, 0.55)
    m.b("lip", -2.2, 2.2, 11.6, 12.4, -2.2, 2.2, GLASS, 0.7)
    m.b("liquid", -3.0, 3.0, 3.6, 10, -3.0, 3.0, A.VIOL, 0.68, True,
        fn=GM.tex_rows([(2, 3), (8, 9)], [(150, 230, 255), (230, 250, 255)]))
    m.b("top_plate", -3.6, 3.6, 9.6, 10.4, -3.6, 3.6, GLASS, 0.6)
    m.b("bot_plate", -3.6, 3.6, 2.8, 3.6, -3.6, 3.6, GLASS, 0.4)
    for i, (x0, x1, z0, z1) in enumerate(((3.0, 3.6, 3.0, 3.6), (-3.6, -3.0, 3.0, 3.6), (3.0, 3.6, -3.6, -3.0), (-3.6, -3.0, -3.6, -3.0))):
        m.b("bar_%d" % i, x0, x1, 3.6, 9.6, z0, z1, GLASS, 0.7, share="bar_0" if i else None)
    m.b("drop_a", -0.4, 0.4, 14.8, 15.6, -0.4, 0.4, A.CYANR, 0.9, True)
    m.b("drop_b", 1.4, 2.0, 15.6, 16.4, -0.3, 0.3, A.VIOL, 0.9, True)
    return m


def fruit():
    m = GM.Model("void_fruit", False, GM.ITEM_TEX, "item/model", 206)
    m.b("plate", -6.2, 6.2, 0, 1, -4.2, 4.2, GM.STEEL_LT, 0.5)
    m.b("cake", -5, 5, 1, 6.2, -2.6, 2.6, CAKE, 0.55,
        fn=GM.tex_rows([(3, 3), (7, 7)], [(120, 70, 28), (200, 140, 70)]))
    m.b("cream", -5.3, 5.3, 6.2, 7.4, -2.9, 2.9, CREAM, 0.6)
    for i, cx in enumerate((-3.0, 0.0, 3.0)):
        m.b("ban_%d" % i, cx - 1.1, cx + 1.1, 7.4, 8.4, -1.1, 1.1, BANANA, 0.6, share="ban_0" if i else None)
    m.b("seed", -0.4, 0.4, 8.4, 8.7, -0.4, 0.4, WOOD, 0.4)
    m.b("drip_n", -3.6, -2.2, 3.2, 6.2, -2.95, -2.6, A.VIOL, 0.7, True)
    m.b("drip_s", 1.8, 3.4, 2.4, 6.2, 2.6, 2.95, A.VIOL, 0.7, True)
    m.b("spark_a", 4.2, 5.0, 9, 9.8, -0.4, 0.4, A.CYANR, 0.9, True)
    m.b("spark_b", -5.4, -4.6, 8, 8.8, -0.4, 0.4, A.PINK, 0.9, True)
    return m


def gateway():
    m = GM.Model("void_gateway", False, GM.BLOCK_TEX, "block/model", 207)
    m.b("base", -8, 8, 0, 2, -8, 8, BRICK, 0.5)
    m.b("step", -7, 7, 2, 4, -7, 7, BRICK, 0.62)
    m.b("rim_n", -7, 7, 4, 4.5, -7, -6, A.GOLD, 0.5)
    m.b("rim_s", -7, 7, 4, 4.5, 6, 7, A.GOLD, 0.5, share="rim_n")
    m.b("rim_w", -7, -6, 4, 4.5, -6, 6, A.GOLD, 0.5)
    m.b("rim_e", 6, 7, 4, 4.5, -6, 6, A.GOLD, 0.5, share="rim_w")
    m.b("inlay_n", -5, 5, 4, 4.3, -4.6, -4.0, A.CYANR, 0.6, True)
    m.b("inlay_s", -5, 5, 4, 4.3, 4.0, 4.6, A.CYANR, 0.6, True, share="inlay_n")
    m.b("inlay_w", -4.6, -4.0, 4, 4.3, -4, 4, A.CYANR, 0.6, True)
    m.b("inlay_e", 4.0, 4.6, 4, 4.3, -4, 4, A.CYANR, 0.6, True, share="inlay_w")
    for i, (x0, x1, z0, z1) in enumerate(((5.2, 7, 5.2, 7), (-7, -5.2, 5.2, 7), (5.2, 7, -7, -5.2), (-7, -5.2, -7, -5.2))):
        m.b("pil_%d" % i, x0, x1, 4.5, 11, z0, z1, BRICK, 0.55, share="pil_0" if i else None)
        m.b("gem_%d" % i, x0 + 0.4, x1 - 0.4, 11, 12.4, z0 + 0.4, z1 - 0.4, A.CYANR, 0.8, True, share="gem_0" if i else None)
    m.b("ring_n", -3.6, 3.6, 8.2, 9.0, -3.6, -2.8, A.VIOL, 0.7, True)
    m.b("ring_s", -3.6, 3.6, 8.2, 9.0, 2.8, 3.6, A.VIOL, 0.7, True, share="ring_n")
    m.b("ring_w", -3.6, -2.8, 8.2, 9.0, -2.8, 2.8, A.VIOL, 0.7, True)
    m.b("ring_e", 2.8, 3.6, 8.2, 9.0, -2.8, 2.8, A.VIOL, 0.7, True, share="ring_w")
    m.b("core_a", -2, 2, 9.6, 13.6, -2, 2, A.PINK, 0.7, True, rot=("y", 45))
    m.b("core_b", -1.4, 1.4, 10.2, 13.0, -1.4, 1.4, WHITE, 0.95, True, rot=("x", 45))
    return m


def flux_block_texture():
    N = 16
    rng = random.Random(11)
    cols = []
    for x in range(16):
        speed = rng.choice([1, 1, 2, 2, 3])
        prof = [0.0] * 16
        for _ in range(rng.choice([2, 3])):
            c0 = rng.randrange(16)
            ln = rng.choice([2, 3, 4])
            for k in range(ln):
                prof[(c0 + k) % 16] = max(prof[(c0 + k) % 16], 1.0 - 0.18 * k)
        cols.append((speed, prof, rng.randrange(16)))
    frames = []
    for f in range(N):
        im = Image.new("RGBA", (16, 16))
        for y in range(16):
            for x in range(16):
                speed, prof, off = cols[x]
                val = prof[(y + f * speed + off) % 16]
                base = 0.25 + 0.2 * vnoise(x, (y + f) % 16, 3.0, 17)
                c = ramp([(30, 12, 90), (80, 40, 190), (120, 90, 235), (170, 235, 255)], min(1.0, base + 0.65 * val))
                alpha = int(150 + 95 * val)
                if x in (0, 15):
                    alpha = min(255, alpha + 20)
                im.putpixel((x, y), (c[0], c[1], c[2], alpha))
        frames.append(im)
    sheet = Image.new("RGBA", (16, 16 * N), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        sheet.paste(fr, (0, 16 * i))
    path = os.path.join(ASSETS, "textures", "block", "void_flux.png")
    sheet.save(path)
    with open(path + ".mcmeta", "w") as fp:
        json.dump({"animation": {"frametime": 2, "interpolate": True}}, fp)


def jw(path, obj):
    full = os.path.join(RES, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fp:
        json.dump(obj, fp, ensure_ascii=False, indent=2)
        fp.write("\n")


def merge_json(path, update, key_list=None):
    full = os.path.join(RES, path)
    data = {}
    if os.path.exists(full):
        with open(full, encoding="utf-8") as fp:
            data = json.load(fp)
    if key_list:
        vals = data.setdefault("values", [])
        for v in update:
            if v not in vals:
                vals.append(v)
        data.setdefault("replace", False)
    else:
        data.update(update)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
        fp.write("\n")


def V(n):
    return NS + ":" + n


def write_models_and_data():
    for fn in (warp_rod, eye, tether, wisp_core, flux_vial, fruit):
        m = fn()
        print("%-18s %3d phan" % (m.name, m.write_item()))
    g = gateway()
    print("%-18s %3d phan" % (g.name, g.write_block("voidrealm:block/void_bricks")))
    flux_block_texture()

    # ---- blockstates + models cho khoi
    jw("assets/voidrealm/blockstates/void_gateway.json", {"variants": {"": {"model": V("block/void_gateway")}}})
    jw("assets/voidrealm/models/item/void_gateway.json", {"parent": V("block/void_gateway")})
    jw("assets/voidrealm/models/block/void_flux.json", {
        "parent": "minecraft:block/cube_all", "render_type": "minecraft:translucent",
        "textures": {"all": V("block/void_flux"), "particle": V("block/void_flux")}})
    jw("assets/voidrealm/blockstates/void_flux.json", {"multipart": [{"apply": {"model": V("block/void_flux")}}]})
    for egg in ("void_wisp", "void_stalker_bird"):
        jw("assets/voidrealm/models/item/%s_spawn_egg.json" % egg, {"parent": "minecraft:item/template_spawn_egg"})

    # ---- lang
    vi = {
        "item.voidrealm.warp_rod": "Trượng Bóp Méo Không Gian",
        "item.voidrealm.eye_of_the_void": "Mắt Nhìn Thực Tại",
        "item.voidrealm.void_tether": "Dây Thừng Trọng Lực",
        "item.voidrealm.wisp_core": "Lõi Void Wisp",
        "item.voidrealm.void_fruit": "Bánh Chuối Hư Không",
        "block.voidrealm.void_gateway": "Máy Dịch Chuyển Tức Thời",
        "block.voidrealm.void_flux": "Thác Nước Ngược (Void Flux)",
        "entity.voidrealm.black_hole": "Lỗ Đen",
        "entity.voidrealm.void_wisp": "Void Wisp",
        "entity.voidrealm.void_stalker_bird": "Chim Rình Rập Hư Không",
        "item.voidrealm.void_wisp_spawn_egg": "Trứng Void Wisp",
        "item.voidrealm.void_stalker_bird_spawn_egg": "Trứng Chim Rình Rập Hư Không",
        "tooltip.voidrealm.warp_rod": "Chuột phải: tạo lỗ đen tại điểm ngắm, hút quái vật vào tâm rồi nổ tung.",
        "tooltip.voidrealm.eye_of_the_void": "Cầm trên tay: thấy quặng xuyên địa hình và mọi sinh vật (kể cả tàng hình) phát sáng.",
        "tooltip.voidrealm.void_tether": "Chuột phải: bắn móc vào khối và tự kéo bạn tới đó. Shift để thả. Có chống rơi sau khi thả.",
        "tooltip.voidrealm.wisp_core": "Chuột phải: gọi Void Wisp soi đường và nhặt đồ rơi xuống vực. Dùng lại để cất đi.",
        "message.voidrealm.tether_miss": "Không có khối nào trong tầm với!",
        "message.voidrealm.gateway_alone": "Cần ít nhất 2 Máy Dịch Chuyển để di chuyển.",
        "message.voidrealm.gateway_missing": "Cổng đích đã biến mất!",
        "message.voidrealm.gateway_fuel": "Cần %s Mảnh Hư Không trong túi đồ để dịch chuyển!",
        "message.voidrealm.gateway_jump": "Dịch chuyển tới %s, %s, %s (-%s Mảnh Hư Không)",
        "message.voidrealm.wisp_summoned": "Void Wisp đã đi theo bạn.",
        "message.voidrealm.wisp_dismissed": "Void Wisp đã trở về.",
    }
    en = {
        "item.voidrealm.warp_rod": "Warp Rod",
        "item.voidrealm.eye_of_the_void": "Eye of the Void",
        "item.voidrealm.void_tether": "Void Tether",
        "item.voidrealm.wisp_core": "Wisp Core",
        "item.voidrealm.void_fruit": "Void Fruit Cake",
        "block.voidrealm.void_gateway": "Void Gateway",
        "block.voidrealm.void_flux": "Void Flux",
        "entity.voidrealm.black_hole": "Black Hole",
        "entity.voidrealm.void_wisp": "Void Wisp",
        "entity.voidrealm.void_stalker_bird": "Void Stalker Bird",
        "item.voidrealm.void_wisp_spawn_egg": "Void Wisp Spawn Egg",
        "item.voidrealm.void_stalker_bird_spawn_egg": "Void Stalker Bird Spawn Egg",
        "tooltip.voidrealm.warp_rod": "Right-click: create a black hole at your aim that drags mobs in, then explodes.",
        "tooltip.voidrealm.eye_of_the_void": "Hold: see ores through terrain and every creature (even invisible) glowing.",
        "tooltip.voidrealm.void_tether": "Right-click: fire a hook at a block and be pulled to it. Sneak to release. Slow fall after release.",
        "tooltip.voidrealm.wisp_core": "Right-click: summon a Void Wisp that lights the way and recovers items falling into the void. Use again to dismiss.",
        "message.voidrealm.tether_miss": "No block in reach!",
        "message.voidrealm.gateway_alone": "You need at least 2 Void Gateways to travel.",
        "message.voidrealm.gateway_missing": "The destination gateway is gone!",
        "message.voidrealm.gateway_fuel": "You need %s Void Shards in your inventory to teleport!",
        "message.voidrealm.gateway_jump": "Teleported to %s, %s, %s (-%s Void Shards)",
        "message.voidrealm.wisp_summoned": "Your Void Wisp follows you.",
        "message.voidrealm.wisp_dismissed": "Your Void Wisp went home.",
    }
    merge_json("assets/voidrealm/lang/vi_vn.json", vi)
    merge_json("assets/voidrealm/lang/en_us.json", en)

    # ---- recipes
    def shaped(name, pattern, key, result, count=1, cat="equipment"):
        jw("data/voidrealm/recipe/%s.json" % name, {
            "type": "minecraft:crafting_shaped", "category": cat, "pattern": pattern,
            "key": {k: {"item": v} for k, v in key.items()}, "result": {"id": result, "count": count}})

    def shapeless(name, ings, result, count=1, cat="misc"):
        jw("data/voidrealm/recipe/%s.json" % name, {
            "type": "minecraft:crafting_shapeless", "category": cat,
            "ingredients": [{"item": i} for i in ings], "result": {"id": result, "count": count}})

    SH, ING, CORE = V("void_shard"), V("void_steel_ingot"), V("rift_core")
    shaped("warp_rod", [" PR", " IP", "I  "], {"P": "minecraft:ender_pearl", "R": CORE, "I": ING}, V("warp_rod"))
    shaped("eye_of_the_void", ["SES", "ECE", "SES"], {"S": SH, "E": "minecraft:ender_eye", "C": CORE}, V("eye_of_the_void"))
    shaped("void_tether", [" I ", "SLS", " I "], {"I": ING, "S": SH, "L": "minecraft:lead"}, V("void_tether"))
    shaped("wisp_core", [" G ", "SCS", " G "], {"G": "minecraft:glowstone_dust", "S": SH, "C": CORE}, V("wisp_core"), cat="misc")
    shapeless("void_fruit", [SH, "minecraft:wheat", "minecraft:wheat", "minecraft:sugar", "minecraft:glow_berries"], V("void_fruit"), 2)
    shaped("void_gateway", ["ICI", "SRS", "BBB"], {"I": ING, "C": "minecraft:ender_eye", "S": SH, "R": CORE, "B": V("void_bricks")},
           V("void_gateway"), cat="building")
    shapeless("void_flux", [SH, SH, "minecraft:ender_pearl", "minecraft:glass_bottle"], V("void_flux"), 1)

    # ---- loot
    jw("data/voidrealm/loot_table/blocks/void_gateway.json", {
        "type": "minecraft:block", "random_sequence": "voidrealm:blocks/void_gateway",
        "pools": [{"rolls": 1.0, "bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:survives_explosion"}],
                   "entries": [{"type": "minecraft:item", "name": V("void_gateway")}]}]})
    jw("data/voidrealm/loot_table/blocks/void_flux.json", {
        "type": "minecraft:block", "random_sequence": "voidrealm:blocks/void_flux",
        "pools": [{"rolls": 1.0, "bonus_rolls": 0.0, "conditions": [
            {"condition": "minecraft:block_state_property", "block": V("void_flux"), "properties": {"age": "0"}}],
            "entries": [{"type": "minecraft:item", "name": V("void_flux")}]}]})
    jw("data/voidrealm/loot_table/entities/void_stalker_bird.json", {
        "type": "minecraft:entity", "pools": [
            {"rolls": 1.0, "bonus_rolls": 0.0, "entries": [{"type": "minecraft:item", "name": "minecraft:feather", "functions": [
                {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1.0, "max": 3.0}}]}]},
            {"rolls": 1.0, "bonus_rolls": 0.0, "conditions": [{"condition": "minecraft:random_chance", "chance": 0.35}],
             "entries": [{"type": "minecraft:item", "name": SH}]}]})

    # ---- tags
    merge_json("data/minecraft/tags/block/mineable/pickaxe.json", [V("void_gateway")], True)
    merge_json("data/minecraft/tags/block/needs_iron_tool.json", [V("void_gateway")], True)
    merge_json("data/c/tags/block/ores.json", [V("void_crystal_ore"), V("deepslate_void_crystal_ore")], True)

    # ---- spawn chim
    for name, biomes in (("spawn_bird_end", "#minecraft:is_end"), ("spawn_bird_mountain", "#minecraft:is_mountain")):
        jw("data/voidrealm/neoforge/biome_modifier/%s.json" % name, {
            "type": "neoforge:add_spawns", "biomes": biomes,
            "spawners": [{"type": V("void_stalker_bird"), "weight": 5, "minCount": 1, "maxCount": 2}]})


if __name__ == "__main__":
    w = build_wisp()
    b = build_bird()
    write_java(w, b)
    print("entity models xong")
    write_models_and_data()
    print("magitech xong")
