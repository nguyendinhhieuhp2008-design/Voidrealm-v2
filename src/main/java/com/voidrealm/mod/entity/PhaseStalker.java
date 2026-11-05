package com.voidrealm.mod.entity;

import com.voidrealm.mod.effect.Fx;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;

/**
 * Ke Rinh Rap Hu Anh: dich chuyen ra sau luc bi danh va "chop" toi gan muc tieu khi o xa.
 */
public class PhaseStalker extends Monster {
    private int blinkCooldown = 40;

    public PhaseStalker(EntityType<? extends PhaseStalker> type, Level level) {
        super(type, level);
        this.xpReward = 12;
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 24.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.3D)
                .add(Attributes.ATTACK_DAMAGE, 6.0D)
                .add(Attributes.FOLLOW_RANGE, 36.0D);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.1D, false));
        this.goalSelector.addGoal(5, new WaterAvoidingRandomStrollGoal(this, 0.8D));
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 8.0F));
        this.goalSelector.addGoal(7, new RandomLookAroundGoal(this));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        LivingEntity target = this.getTarget();
        if (target != null && this.blinkCooldown > 0) {
            this.blinkCooldown--;
        }
        if (target != null && this.blinkCooldown <= 0 && this.distanceToSqr(target) > 36.0D) {
            double angle = this.random.nextDouble() * Math.PI * 2.0D;
            double tx = target.getX() + Math.cos(angle) * 3.0D;
            double tz = target.getZ() + Math.sin(angle) * 3.0D;
            if (this.randomTeleport(tx, target.getY(), tz, true)) {
                this.playSound(SoundEvents.ENDERMAN_TELEPORT, 1.0F, 1.0F);
                Fx.deathBurst(this, ParticleTypes.PORTAL);
            }
            this.blinkCooldown = 80 + this.random.nextInt(60);
        }
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        boolean result = super.hurt(source, amount);
        if (result && !this.level().isClientSide && this.isAlive() && this.random.nextFloat() < 0.35F) {
            double x = this.getX() + (this.random.nextDouble() - 0.5D) * 12.0D;
            double y = this.getY() + (double) (this.random.nextInt(5) - 2);
            double z = this.getZ() + (this.random.nextDouble() - 0.5D) * 12.0D;
            if (this.randomTeleport(x, y, z, true)) {
                this.playSound(SoundEvents.ENDERMAN_TELEPORT, 1.0F, 1.0F);
                Fx.deathBurst(this, ParticleTypes.PORTAL);
            }
        }
        return result;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.ENDERMAN_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.ENDERMAN_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.ENDERMAN_DEATH;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (this.level().isClientSide) {
            Fx.aura(this, ParticleTypes.PORTAL, 2);
        }
    }

    @Override
    public void die(DamageSource source) {
        super.die(source);
        Fx.deathBurst(this, ParticleTypes.PORTAL);
    }
}
