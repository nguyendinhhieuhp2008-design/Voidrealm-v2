#!/usr/bin/env python3
"""Dream Crystal: quang xanh duong + vu khi + giap bay + nu.  Chay SAU gen_art/gen_armor/gen_blocks, TRUOC gen_realm.
Texture lay tu bo Thep Hu Khong roi doi mau sang xanh duong (khop phong cach), them icon rieng cho tinh the / quang / no.
"""
import colorsys
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RES = os.path.join(ROOT, "src", "main", "resources")
A = os.path.join(RES, "assets", "voidrealm")
TEX = os.path.join(A, "textures")
NS = "voidrealm"


def V(n):
    return NS + ":" + n


def jw(path, obj):
    full = os.path.join(RES, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fp:
        json.dump(obj, fp, ensure_ascii=False, indent=2)
        fp.write("\n")


def merge(path, update, tag=False):
    full = os.path.join(RES, path)
    data = {}
    if os.path.exists(full):
        with open(full, encoding="utf-8") as fp:
            data = json.load(fp)
    if tag:
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


# ------------------------------------------------------------------ doi mau -> xanh duong
def to_blue(img, lift=1.0):
    img = img.convert("RGBA")
    out = Image.new("RGBA", img.size)
    src, dst = img.load(), out.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = src[x, y]
            if a == 0:
                dst[x, y] = (0, 0, 0, 0)
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s < 0.12:                                   # xam/trang -> hoi xanh
                h, s = 0.58, max(s, 0.18)
            elif 0.04 <= h <= 0.2:                         # vang (vien) -> xanh ngoc sang
                h, s, v = 0.5, 0.55 * s, min(1.0, v * 1.1)
            elif 0.4 <= h <= 0.55:                         # cyan co san -> trang xanh
                h, s, v = 0.53, s * 0.7, min(1.0, v * 1.05)
            else:                                          # tim/hong -> xanh duong
                h = 0.60 + (((h - 0.75 + 0.5) % 1.0) - 0.5) * 0.35
                s = min(1.0, s * 1.12 + 0.05)
                v = min(1.0, v * 1.08)
            if lift != 1.0 and v > 0.12:
                v = min(1.0, v * lift + 0.05)
                s = min(s, 0.85)
            rr, gg, bb = colorsys.hsv_to_rgb(h % 1.0, s, v)
            dst[x, y] = (int(rr * 255), int(gg * 255), int(bb * 255), a)
    return out


def recolor(src, dst, lift=1.6):
    im = Image.open(os.path.join(TEX, src))
    to_blue(im, lift).save(os.path.join(TEX, dst))


BLUE = [(8, 24, 80), (20, 60, 170), (50, 120, 240), (110, 190, 255), (220, 245, 255)]


def gem_icon():
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    outline = (6, 16, 56, 255)
    # tinh the chinh (luc giac keo dai)
    top, rt, rb, bot, lb, lt = (8, 1), (12, 5), (12, 10), (8, 14), (4, 10), (4, 5)
    d.polygon([top, rt, rb, bot, lb, lt], fill=BLUE[2] + (255,), outline=outline)
    d.polygon([top, rt, (8, 6)], fill=BLUE[4] + (255,))
    d.polygon([top, lt, (8, 6)], fill=BLUE[3] + (255,))
    d.polygon([lt, (8, 6), (8, 14), lb], fill=BLUE[1] + (255,))
    d.polygon([rt, (8, 6), (8, 14), rb], fill=BLUE[2] + (255,))
    d.polygon([(8, 6), (10, 8), (8, 14)], fill=BLUE[3] + (255,))
    d.line([top, rt, rb, bot, lb, lt, top], fill=outline)
    for p in ((7, 3), (6, 7)):
        im.putpixel(p, (255, 255, 255, 255))
    # manh nho ben canh
    d.polygon([(13, 11), (15, 13), (13, 15), (11, 13)], fill=BLUE[3] + (255,), outline=outline)
    im.putpixel((13, 12), (255, 255, 255, 255))
    d.polygon([(1, 9), (3, 11), (1, 13), (0, 11)], fill=BLUE[2] + (255,), outline=outline)
    im.save(os.path.join(TEX, "item", "dream_crystal.png"))
    return im


def drill_icon():
    """Mui khoan Dream Crystal 2D: tay cam nau-xanh, than may xanh duong, mui khoan xoan oc o goc tren phai."""
    S = 4
    im = Image.new("RGBA", (16 * S, 16 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    dark, mid, lite, white = (6, 16, 56, 255), (30, 80, 200, 255), (110, 190, 255, 255), (235, 250, 255, 255)
    wood, wood_l = (40, 36, 70, 255), (84, 78, 140, 255)

    def L(p, q, col, w=1):
        d.line([(p[0] * S + S // 2, p[1] * S + S // 2), (q[0] * S + S // 2, q[1] * S + S // 2)], fill=col, width=w * S)
    L((1, 14), (7, 8), dark, 3)                    # tay cam
    L((1, 14), (7, 8), wood, 2)
    L((2, 13), (6, 9), wood_l, 1)
    L((6, 9), (10, 5), dark, 6)                    # than may
    L((6, 9), (10, 5), mid, 4)
    L((6, 8), (9, 5), lite, 1)
    d.rectangle([7 * S, 8 * S, 8 * S + S - 1, 9 * S + S - 1], fill=white)   # tinh the nang luong
    # mui khoan (hinh non xoan oc)
    d.polygon([(10 * S, 3 * S), (12 * S, 5 * S), (15 * S, 0), (15 * S + S - 1, 0)], fill=dark)
    L((11, 4), (15, 0), lite, 2)
    for k in range(3):
        a = (11 + k, 4 - k)
        L(a, (a[0] + 1, a[1] - 1), white, 1)
    small = im.resize((16, 16), Image.NEAREST)
    px = small.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255 if a > 100 else 0)
    small.save(os.path.join(TEX, "item", "dream_drill.png"))


def crossbow_icon():
    S = 4
    im = Image.new("RGBA", (16 * S, 16 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    dark, mid, lite, white = (6, 16, 56, 255), (30, 80, 200, 255), (110, 190, 255, 255), (235, 250, 255, 255)
    wood, wood_l = (40, 36, 70, 255), (84, 78, 140, 255)

    def L(p, q, col, w=1):
        d.line([(p[0] * S + S // 2, p[1] * S + S // 2), (q[0] * S + S // 2, q[1] * S + S // 2)], fill=col, width=w * S)
    # bau (tu duoi trai len giua)
    L((2, 14), (9, 7), dark, 3)
    L((2, 14), (9, 7), wood, 2)
    L((3, 13), (8, 8), wood_l, 1)
    # canh cung (cung cong ve phia truoc)
    pts = [(4, 3), (9, 2), (13, 5), (14, 10)]
    L(pts[0], pts[1], dark, 3); L(pts[1], pts[2], dark, 3); L(pts[2], pts[3], dark, 3)
    L(pts[0], pts[1], mid, 2); L(pts[1], pts[2], mid, 2); L(pts[2], pts[3], mid, 2)
    L((5, 3), (9, 2), lite, 1); L((10, 3), (13, 5), lite, 1)
    # day cung
    L((4, 3), (9, 7), white, 1)
    L((14, 10), (9, 7), white, 1)
    # mui ten
    L((9, 7), (13, 3), lite, 1)
    d.polygon([(12 * S, 2 * S), (15 * S, 1 * S), (14 * S, 4 * S)], fill=white)
    # tinh the tren bau
    d.rectangle([6 * S, 9 * S, 7 * S + S - 1, 10 * S + S - 1], fill=lite)
    d.rectangle([6 * S + 1, 9 * S + 1, 6 * S + S, 9 * S + S], fill=white)
    small = im.resize((16, 16), Image.NEAREST)
    # nhan pixel > nua alpha, tranh vien mo
    px = small.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 255 if a > 100 else 0)
    small.save(os.path.join(TEX, "item", "dream_crossbow.png"))


def ore_texture():
    base = Image.open(os.path.join(TEX, "block", "void_stone.png")).convert("RGBA").crop((0, 0, 16, 16))
    base = to_blue(base)
    px = base.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            gg = (r + g + b) / 3 * 0.72
            px[x, y] = (int(gg * 0.85), int(gg * 0.92), int(min(255, gg * 1.12)), 255)
    rnd = random.Random(2026)
    shapes = [[(0, 0), (0, 1), (0, 2), (1, 1), (-1, 1)], [(0, 0), (1, 0), (0, 1), (1, 1), (1, 2)],
              [(0, 0), (0, 1), (1, 1), (-1, 2), (0, 2)], [(0, 0), (1, 0), (1, 1)]]
    centers = [(4, 4), (11, 4), (7, 10), (13, 12), (2, 12), (10, 8)]
    crystals = []
    for cx, cy in centers:
        for (dx, dy) in rnd.choice(shapes):
            x, y = cx + dx, cy + dy
            if 0 <= x < 16 and 0 <= y < 16:
                crystals.append((x, y))
    cset = set(crystals)
    frames = []
    for f in range(8):
        fr = base.copy()
        p = fr.load()
        for (x, y) in crystals:
            edge = any((x + ax, y + ay) not in cset for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            lightness = 3 if (x + y) % 2 == 0 else 4
            col = BLUE[2] if edge else BLUE[lightness]
            if (x - y + f) % 8 == 0 and not edge:
                col = BLUE[4]
            p[x, y] = col + (255,)
        # vien sang
        for (x, y) in crystals:
            if (x * 7 + y * 3 + f * 3) % 19 == 0:
                p[x, y] = (255, 255, 255, 255)
        frames.append(fr)
    sheet = Image.new("RGBA", (16, 16 * len(frames)))
    for i, fr in enumerate(frames):
        sheet.paste(fr, (0, 16 * i))
    path = os.path.join(TEX, "block", "dream_crystal_ore.png")
    sheet.save(path)
    with open(path + ".mcmeta", "w") as fp:
        json.dump({"animation": {"frametime": 4, "interpolate": True}}, fp)


def make_textures():
    recolor("item/void_steel_sword.png", "item/dream_sword.png")
    recolor("item/void_steel_axe.png", "item/dream_battle_axe.png")
    drill_icon()
    for piece in ("helmet", "chestplate", "leggings", "boots"):
        recolor("item/void_steel_%s.png" % piece, "item/dream_%s.png" % piece)
    for layer in (1, 2):
        recolor("models/armor/void_steel_layer_%d.png" % layer, "models/armor/dream_layer_%d.png" % layer)
    gem_icon()
    crossbow_icon()
    ore_texture()
    # icon phang ngoai GUI khong dung (item dung model 3D), nhung giu ban hue cho tien tham khao


def models():
    flat = ["void_steel_sword", "void_steel_axe", "void_steel_pickaxe", "void_steel_shovel", "void_steel_hoe",
            "rift_blade", "void_reaper", "voidpiercer", "gravity_staff", "dream_sword", "dream_battle_axe", "dream_drill"]
    for n in flat:
        jw("assets/voidrealm/models/item/%s.json" % n, {"parent": "minecraft:item/handheld", "textures": {"layer0": V("item/" + n)}})
    for n in ("dream_crystal", "dream_crossbow", "dream_helmet", "dream_chestplate", "dream_leggings", "dream_boots"):
        jw("assets/voidrealm/models/item/%s.json" % n, {"parent": "minecraft:item/generated", "textures": {"layer0": V("item/" + n)}})
    jw("assets/voidrealm/models/block/dream_crystal_ore.json", {"parent": "minecraft:block/cube_all", "textures": {"all": V("block/dream_crystal_ore")}})
    jw("assets/voidrealm/blockstates/dream_crystal_ore.json", {"variants": {"": {"model": V("block/dream_crystal_ore")}}})
    jw("assets/voidrealm/models/item/dream_crystal_ore.json", {"parent": V("block/dream_crystal_ore")})


def data():
    vi = {
        "block.voidrealm.dream_crystal_ore": "Quặng Dream Crystal",
        "item.voidrealm.dream_crystal": "Dream Crystal (Tinh Thể Mộng)",
        "item.voidrealm.dream_sword": "Kiếm Mộng Tinh",
        "item.voidrealm.dream_battle_axe": "Rìu Chiến Mộng Tinh",
        "item.voidrealm.dream_crossbow": "Nỏ Mộng Tinh",
        "item.voidrealm.dream_helmet": "Mũ Mộng Tinh",
        "item.voidrealm.dream_chestplate": "Giáp Cánh Mộng Tinh",
        "item.voidrealm.dream_leggings": "Quần Mộng Tinh",
        "item.voidrealm.dream_boots": "Giày Mộng Tinh",
        "item.voidrealm.dream_drill": "Mũi Khoan Mộng Tinh",
        "message.voidrealm.drill_on": "Mũi khoan: chế độ đào 3x3 BẬT",
        "message.voidrealm.drill_off": "Mũi khoan: chế độ đào 3x3 TẮT",
        "key.categories.voidrealm": "Void Realm",
        "key.voidrealm.boost": "Giáp Mộng Tinh: tăng tốc khi bay",
        "key.voidrealm.tentacle": "Giáp Mộng Tinh: xúc tu tấn công",
        "message.voidrealm.dream_need_flight": "Phải đang bay (lướt) mới tăng tốc được!",
        "message.voidrealm.dream_need_set": "Cần mặc đủ bộ giáp Mộng Tinh.",
        "message.voidrealm.dream_no_target": "Không có kẻ địch trong phạm vi 8 block.",
    }
    en = {
        "block.voidrealm.dream_crystal_ore": "Dream Crystal Ore",
        "item.voidrealm.dream_crystal": "Dream Crystal",
        "item.voidrealm.dream_sword": "Dream Sword",
        "item.voidrealm.dream_battle_axe": "Dream Battle Axe",
        "item.voidrealm.dream_crossbow": "Dream Crossbow",
        "item.voidrealm.dream_helmet": "Dream Helmet",
        "item.voidrealm.dream_chestplate": "Dream Wing Chestplate",
        "item.voidrealm.dream_leggings": "Dream Leggings",
        "item.voidrealm.dream_boots": "Dream Boots",
        "item.voidrealm.dream_drill": "Dream Crystal Drill",
        "message.voidrealm.drill_on": "Drill: 3x3 mining mode ON",
        "message.voidrealm.drill_off": "Drill: 3x3 mining mode OFF",
        "key.categories.voidrealm": "Void Realm",
        "key.voidrealm.boost": "Dream Armor: flight boost",
        "key.voidrealm.tentacle": "Dream Armor: tentacle strike",
        "message.voidrealm.dream_need_flight": "You must be gliding to boost!",
        "message.voidrealm.dream_need_set": "You need the full Dream armor set.",
        "message.voidrealm.dream_no_target": "No enemies within 8 blocks.",
    }
    merge("assets/voidrealm/lang/vi_vn.json", vi)
    merge("assets/voidrealm/lang/en_us.json", en)

    def shaped(name, pattern, key, result, count=1, cat="equipment"):
        jw("data/voidrealm/recipe/%s.json" % name, {
            "type": "minecraft:crafting_shaped", "category": cat, "pattern": pattern,
            "key": {k: {"item": v} for k, v in key.items()}, "result": {"id": result, "count": count}})
    D, ST, ING, SILK = V("dream_crystal"), "minecraft:stick", V("void_steel_ingot"), V("phase_silk")
    shaped("dream_sword", ["D", "D", "S"], {"D": D, "S": ST}, V("dream_sword"))
    shaped("dream_battle_axe", ["DD", "DS", "IS"], {"D": D, "S": ST, "I": ING}, V("dream_battle_axe"))
    shaped("dream_crossbow", ["IDI", "SCS", " D "], {"I": ING, "D": D, "S": "minecraft:string", "C": "minecraft:crossbow"},
           V("dream_crossbow"))
    shaped("dream_drill", ["DDD", "DPD", " I "], {"D": D, "P": V("void_steel_pickaxe"), "I": ING}, V("dream_drill"))
    shaped("dream_helmet", ["DDD", "D D"], {"D": D}, V("dream_helmet"))
    shaped("dream_chestplate", ["D D", "DSD", "DDD"], {"D": D, "S": SILK}, V("dream_chestplate"))
    shaped("dream_leggings", ["DDD", "D D", "D D"], {"D": D}, V("dream_leggings"))
    shaped("dream_boots", ["D D", "D D"], {"D": D}, V("dream_boots"))

    silk = {"condition": "minecraft:match_tool", "predicate": {"predicates": {"minecraft:enchantments": [
        {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}}}
    jw("data/voidrealm/loot_table/blocks/dream_crystal_ore.json", {
        "type": "minecraft:block", "random_sequence": "voidrealm:blocks/dream_crystal_ore",
        "pools": [{"rolls": 1.0, "bonus_rolls": 0.0, "entries": [{"type": "minecraft:alternatives", "children": [
            {"type": "minecraft:item", "name": V("dream_crystal_ore"), "conditions": [silk]},
            {"type": "minecraft:item", "name": D, "functions": [
                {"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": 1.0, "max": 2.0}},
                {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune", "formula": "minecraft:ore_drops"},
                {"function": "minecraft:explosion_decay"}]}]}]}]})
    merge("data/minecraft/tags/block/mineable/pickaxe.json", [V("dream_crystal_ore")], True)
    merge("data/minecraft/tags/block/needs_diamond_tool.json", [V("dream_crystal_ore")], True)
    merge("data/c/tags/block/ores.json", [V("dream_crystal_ore")], True)
    merge("data/minecraft/tags/item/swords.json", [V("dream_sword")], True)
    merge("data/minecraft/tags/item/pickaxes.json", [V("dream_drill")], True)
    merge("data/minecraft/tags/item/axes.json", [V("dream_battle_axe")], True)
    merge("data/minecraft/tags/item/head_armor.json", [V("dream_helmet")], True)
    merge("data/minecraft/tags/item/chest_armor.json", [V("dream_chestplate")], True)
    merge("data/minecraft/tags/item/leg_armor.json", [V("dream_leggings")], True)
    merge("data/minecraft/tags/item/foot_armor.json", [V("dream_boots")], True)
    arm = [V("dream_helmet"), V("dream_chestplate"), V("dream_leggings"), V("dream_boots")]
    allt = arm + [V("dream_sword"), V("dream_battle_axe"), V("dream_crossbow"), V("dream_drill")]
    merge("data/minecraft/tags/item/enchantable/armor.json", arm, True)
    merge("data/minecraft/tags/item/enchantable/head_armor.json", [arm[0]], True)
    merge("data/minecraft/tags/item/enchantable/chest_armor.json", [arm[1]], True)
    merge("data/minecraft/tags/item/enchantable/leg_armor.json", [arm[2]], True)
    merge("data/minecraft/tags/item/enchantable/foot_armor.json", [arm[3]], True)
    merge("data/minecraft/tags/item/enchantable/durability.json", allt, True)
    merge("data/minecraft/tags/item/enchantable/sword.json", [V("dream_sword")], True)
    merge("data/minecraft/tags/item/enchantable/weapon.json", [V("dream_sword"), V("dream_battle_axe")], True)
    merge("data/minecraft/tags/item/enchantable/sharp_weapon.json", [V("dream_sword"), V("dream_battle_axe")], True)
    merge("data/minecraft/tags/item/enchantable/crossbow.json", [V("dream_crossbow")], True)


if __name__ == "__main__":
    make_textures()
    models()
    data()
    print("gen_dream xong")
