package com.voidrealm.mod;

import net.minecraft.util.RandomSource;
import net.neoforged.neoforge.common.ModConfigSpec;

/**
 * Cau hinh chung (config/voidrealm-common.toml).
 * Gia tri mac dinh duoc chon nhe cho thiet bi di dong (Zalith Launcher 2).
 */
public class Config {
    private static final ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();

    public static final ModConfigSpec.IntValue PARTICLE_PERCENT = BUILDER
            .comment("Ti le hat (particle) cua cac chieu thuc, 0-100. Giam xuong de choi muot hon tren dien thoai.")
            .defineInRange("particlePercent", 50, 0, 100);

    public static final ModConfigSpec.BooleanValue ARMOR_SET_BONUS = BUILDER
            .comment("Bat/tat hieu ung khi mac du bo giap (Thep Hu Khong, Hu Anh).")
            .define("armorSetBonus", true);

    public static final ModConfigSpec.IntValue BLINK_RANGE = BUILDER
            .comment("Tam dich chuyen toi da cua Kiem Xe Khong Gian (o).")
            .defineInRange("blinkRange", 8, 2, 16);

    public static final ModConfigSpec.IntValue BLINK_COOLDOWN_TICKS = BUILDER
            .comment("Thoi gian hoi chieu Kiem Xe Khong Gian (tick, 20 tick = 1 giay).")
            .defineInRange("blinkCooldownTicks", 60, 0, 1200);

    public static final ModConfigSpec.IntValue GRAVITY_RADIUS = BUILDER
            .comment("Ban kinh keo cua Truong Trong Luc (o).")
            .defineInRange("gravityStaffRadius", 10, 3, 24);

    public static final ModConfigSpec.IntValue GRAVITY_COOLDOWN_TICKS = BUILDER
            .comment("Thoi gian hoi chieu Truong Trong Luc (tick).")
            .defineInRange("gravityStaffCooldownTicks", 160, 0, 2400);

    public static final ModConfigSpec.BooleanValue BOSS_SUMMONS_MINIONS = BUILDER
            .comment("Chua Te Hu Khong co goi dong bon (Ke Rinh Rap Hu Anh) hay khong.")
            .define("bossSummonsMinions", true);

    public static final ModConfigSpec SPEC = BUILDER.build();

    /** Tinh so hat thuc te theo ti le cau hinh. */
    public static int particles(int base) {
        int percent = PARTICLE_PERCENT.get();
        return Math.max(0, base * percent / 100);
    }

    /** Xac suat ra hat: trung binh 1/oneIn moi lan goi, nhan voi ti le hat trong cau hinh. */
    public static boolean roll(RandomSource random, int oneIn) {
        int percent = PARTICLE_PERCENT.get();
        return percent > 0 && random.nextInt(100) < percent && random.nextInt(Math.max(1, oneIn)) == 0;
    }

    private Config() {
    }
}
