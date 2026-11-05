package com.voidrealm.mod.effect;

import com.voidrealm.mod.Config;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.phys.Vec3;

/**
 * Cac hieu ung hat dung chung. Moi ham deu ton trong cau hinh "particlePercent"
 * de nguoi choi dien thoai (Zalith Launcher 2) co the giam bot.
 */
public final class Fx {

    /** Hat quanh than thuc the (goi o phia client, trong aiStep). oneIn = trung binh moi bao nhieu tick moi ra 1 hat. */
    public static void aura(Entity entity, ParticleOptions particle, int oneIn) {
        RandomSource random = entity.getRandom();
        if (Config.roll(random, oneIn)) {
            entity.level().addParticle(particle, entity.getRandomX(0.6D), entity.getRandomY(), entity.getRandomZ(0.6D),
                    0.0D, 0.03D, 0.0D);
        }
    }

    /** No hat quanh mot thuc the (phia may chu). */
    public static void deathBurst(Entity entity, ParticleOptions particle) {
        if (entity.level() instanceof ServerLevel level) {
            burst(level, entity.getX(), entity.getY() + entity.getBbHeight() * 0.5D, entity.getZ(),
                    particle, 28, Math.max(0.3D, entity.getBbWidth() * 0.5D), 0.08D);
        }
    }

    public static void burst(ServerLevel level, double x, double y, double z, ParticleOptions particle,
                             int baseCount, double spread, double speed) {
        int count = Config.particles(baseCount);
        if (count > 0) {
            level.sendParticles(particle, x, y, z, count, spread, spread, spread, speed);
        }
    }

    /** Vong hat lan toa ra (speed duong) hoac thu vao (speed am) tren mat phang ngang. */
    public static void ring(ServerLevel level, double x, double y, double z, double radius,
                            ParticleOptions particle, int basePoints, double speed) {
        int points = Config.particles(basePoints);
        if (points <= 0) {
            return;
        }
        for (int i = 0; i < points; i++) {
            double angle = (Math.PI * 2.0D) * i / points;
            double cos = Math.cos(angle);
            double sin = Math.sin(angle);
            level.sendParticles(particle, x + cos * radius, y, z + sin * radius, 0, cos, 0.0D, sin, speed);
        }
    }

    /** Duong hat noi hai diem (vet kiem, tia giao...). */
    public static void line(ServerLevel level, Vec3 from, Vec3 to, ParticleOptions particle, double step) {
        Vec3 delta = to.subtract(from);
        double length = delta.length();
        if (length < 1.0E-3D) {
            return;
        }
        Vec3 dir = delta.scale(1.0D / length);
        RandomSource random = level.getRandom();
        for (double d = 0.0D; d <= length; d += step) {
            if (random.nextInt(100) < Config.PARTICLE_PERCENT.get()) {
                Vec3 p = from.add(dir.scale(d));
                level.sendParticles(particle, p.x, p.y, p.z, 1, 0.05D, 0.05D, 0.05D, 0.0D);
            }
        }
    }

    private Fx() {
    }
}
