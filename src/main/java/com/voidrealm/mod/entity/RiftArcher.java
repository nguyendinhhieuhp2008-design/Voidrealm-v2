package com.voidrealm.mod.entity;

import com.voidrealm.mod.effect.Fx;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Skeleton;
import net.minecraft.world.level.Level;

/**
 * Cung Thu Di Gioi: ban cung tu xa, khong chay nang nhu xuong thuong.
 * Ke thua Skeleton cua vanilla de dung lai AI ban cung, am thanh va cach cam cung
 * (khong phai viet lai, va khong phu thuoc vao cac ham package-private cua AbstractSkeleton).
 */
public class RiftArcher extends Skeleton {
    public RiftArcher(EntityType<? extends RiftArcher> type, Level level) {
        super(type, level);
        this.xpReward = 10;
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Skeleton.createAttributes()
                .add(Attributes.MAX_HEALTH, 26.0D)
                .add(Attributes.FOLLOW_RANGE, 40.0D);
    }

    /** Khong chay nang. */
    @Override
    public boolean isSunBurnTick() {
        return false;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (this.level().isClientSide) {
            Fx.aura(this, ParticleTypes.SOUL_FIRE_FLAME, 9);
        }
    }

    @Override
    public void die(DamageSource source) {
        super.die(source);
        Fx.deathBurst(this, ParticleTypes.SOUL_FIRE_FLAME);
    }
}
