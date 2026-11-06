package com.voidrealm.mod.entity;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.effect.Fx;
import java.util.List;
import java.util.UUID;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Lo den do Truong Bop Me Khong Gian tao ra: hut moi sinh vat (tru nguoi choi) ve tam,
 * gay sat thuong o gan tam va no tung ra khi het gio.
 */
public class BlackHole extends Entity {
    public static final int LIFETIME = 110;
    private static final double RADIUS = 9.0D;

    private UUID ownerId;

    public BlackHole(EntityType<? extends BlackHole> type, Level level) {
        super(type, level);
        this.noPhysics = true;
    }

    public void setOwner(Player owner) {
        this.ownerId = owner.getUUID();
    }

    @Override
    protected void defineSynchedData(SynchedEntityData.Builder builder) {
    }

    @Override
    public boolean isPickable() {
        return false;
    }

    @Override
    public void tick() {
        super.tick();
        if (this.level().isClientSide) {
            clientFx();
            return;
        }
        ServerLevel level = (ServerLevel) this.level();
        double cx = this.getX();
        double cy = this.getY();
        double cz = this.getZ();

        if (this.tickCount == 1) {
            level.playSound(null, cx, cy, cz, SoundEvents.ENDER_DRAGON_GROWL, SoundSource.PLAYERS, 0.5F, 1.8F);
        }
        if (this.tickCount % 22 == 0) {
            level.playSound(null, cx, cy, cz, SoundEvents.PORTAL_AMBIENT, SoundSource.PLAYERS, 0.7F, 0.6F);
        }

        List<LivingEntity> victims = level.getEntitiesOfClass(LivingEntity.class,
                this.getBoundingBox().inflate(RADIUS),
                e -> e.isAlive() && !(e instanceof Player));
        for (LivingEntity e : victims) {
            Vec3 to = new Vec3(cx, cy, cz).subtract(e.position().add(0.0D, e.getBbHeight() * 0.5D, 0.0D));
            double dist = to.length();
            if (dist < 0.05D || dist > RADIUS) {
                continue;
            }
            double strength = 0.10D + (1.0D - dist / RADIUS) * 0.38D;
            Vec3 pull = to.scale(1.0D / dist).scale(strength);
            e.setDeltaMovement(e.getDeltaMovement().scale(0.65D).add(pull));
            e.hurtMarked = true;
            e.fallDistance = 0.0F;
            if (dist < 1.8D && this.tickCount % 8 == 0) {
                e.hurt(level.damageSources().magic(), 3.0F);
            }
        }

        // vong hat hut vao theo hinh xoan oc
        if (this.tickCount % 2 == 0) {
            double spin = this.tickCount * 0.35D;
            Fx.ring(level, cx, cy, cz, 3.2D, ParticleTypes.REVERSE_PORTAL, 14, -0.25D);
            Fx.ring(level, cx, cy + 0.2D * Math.sin(spin), cz, 6.0D, ParticleTypes.PORTAL, 10, -0.45D);
        }

        if (this.tickCount >= LIFETIME) {
            for (LivingEntity e : victims) {
                if (e.position().distanceToSqr(cx, cy, cz) < 16.0D) {
                    e.hurt(level.damageSources().magic(), 8.0F);
                }
            }
            Fx.burst(level, cx, cy, cz, ParticleTypes.END_ROD, 60, 0.9D, 0.35D);
            Fx.burst(level, cx, cy, cz, ParticleTypes.EXPLOSION, 3, 0.8D, 0.0D);
            Fx.ring(level, cx, cy, cz, 1.0D, ParticleTypes.DRAGON_BREATH, 30, 0.35D);
            level.playSound(null, cx, cy, cz, SoundEvents.GENERIC_EXPLODE.value(), SoundSource.PLAYERS, 0.8F, 1.5F);
            this.discard();
        }
    }

    private void clientFx() {
        Level level = this.level();
        double cx = this.getX();
        double cy = this.getY();
        double cz = this.getZ();
        double t = this.tickCount * 0.4D;
        // loi den
        for (int i = 0; i < 2; i++) {
            if (Config.roll(this.random, 1)) {
                level.addParticle(ParticleTypes.SQUID_INK,
                        cx + (this.random.nextDouble() - 0.5D) * 0.7D, cy + (this.random.nextDouble() - 0.5D) * 0.7D,
                        cz + (this.random.nextDouble() - 0.5D) * 0.7D, 0.0D, 0.0D, 0.0D);
            }
        }
        // dia bồi tụ: hat xoay quanh
        for (int i = 0; i < 3; i++) {
            if (Config.roll(this.random, 1)) {
                double a = t + i * 2.1D + this.random.nextDouble();
                double r = 1.0D + this.random.nextDouble() * 1.8D;
                level.addParticle(this.random.nextBoolean() ? ParticleTypes.END_ROD : ParticleTypes.DRAGON_BREATH,
                        cx + Math.cos(a) * r, cy + (this.random.nextDouble() - 0.5D) * 0.15D, cz + Math.sin(a) * r,
                        -Math.sin(a) * 0.12D, 0.0D, Math.cos(a) * 0.12D);
            }
        }
    }

    @Override
    protected void readAdditionalSaveData(CompoundTag tag) {
        if (tag.hasUUID("Owner")) {
            this.ownerId = tag.getUUID("Owner");
        }
        this.tickCount = tag.getInt("Age");
    }

    @Override
    protected void addAdditionalSaveData(CompoundTag tag) {
        if (this.ownerId != null) {
            tag.putUUID("Owner", this.ownerId);
        }
        tag.putInt("Age", this.tickCount);
    }
}
