package com.voidrealm.mod.entity;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.effect.Fx;
import com.voidrealm.mod.registry.ModEntities;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobSpawnType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Chua Te Hu Khong: boss cua Thanh Tri Hu Khong.
 * - Co thanh mau boss.
 * - Dinh ky phat "xung hu khong" day lui va lam toi man hinh nguoi choi gan.
 * - Goi dong bon Ke Rinh Rap Hu Anh (co the tat trong config).
 * - Duoi 50% mau: nong gian, chay nhanh hon va phat xung nhanh hon.
 */
public class VoidSovereign extends Monster {
    private final ServerBossEvent bossEvent = new ServerBossEvent(
            this.getDisplayName(), BossEvent.BossBarColor.PURPLE, BossEvent.BossBarOverlay.NOTCHED_10);

    private int pulseTimer = 120;
    private int summonTimer = 200;
    private boolean enraged = false;

    public VoidSovereign(EntityType<? extends VoidSovereign> type, Level level) {
        super(type, level);
        this.xpReward = 250;
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, 300.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.28D)
                .add(Attributes.ATTACK_DAMAGE, 14.0D)
                .add(Attributes.ARMOR, 10.0D)
                .add(Attributes.KNOCKBACK_RESISTANCE, 0.9D)
                .add(Attributes.FOLLOW_RANGE, 48.0D);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.1D, true));
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 16.0F));
        this.goalSelector.addGoal(7, new RandomLookAroundGoal(this));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
    }

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        this.bossEvent.setProgress(this.getHealth() / this.getMaxHealth());

        if (!(this.level() instanceof ServerLevel serverLevel)) {
            return;
        }

        if (!this.enraged && this.getHealth() < this.getMaxHealth() * 0.5F) {
            this.enraged = true;
            this.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, MobEffectInstance.INFINITE_DURATION, 0, false, false));
            serverLevel.playSound(null, this.getX(), this.getY(), this.getZ(),
                    SoundEvents.ENDER_DRAGON_GROWL, SoundSource.HOSTILE, 2.0F, 0.8F);
            Fx.burst(serverLevel, this.getX(), this.getY() + 1.8D, this.getZ(), ParticleTypes.SOUL_FIRE_FLAME, 60, 1.2D, 0.15D);
            Fx.ring(serverLevel, this.getX(), this.getY() + 0.3D, this.getZ(), 1.0D, ParticleTypes.END_ROD, 48, 0.7D);
        }

        if (this.getTarget() == null) {
            return;
        }

        if (--this.pulseTimer <= 0) {
            this.voidPulse(serverLevel);
            this.pulseTimer = this.enraged ? 100 : 140;
        }

        if (Config.BOSS_SUMMONS_MINIONS.get() && --this.summonTimer <= 0) {
            this.summonMinions(serverLevel);
            this.summonTimer = this.enraged ? 220 : 320;
        }
    }

    private void voidPulse(ServerLevel level) {
        AABB area = this.getBoundingBox().inflate(9.0D, 4.0D, 9.0D);
        List<Player> players = level.getEntitiesOfClass(Player.class, area,
                player -> player.isAlive() && !player.isSpectator() && !player.isCreative());
        for (Player player : players) {
            player.hurt(this.damageSources().indirectMagic(this, this), 8.0F);
            Vec3 away = player.position().subtract(this.position());
            Vec3 flat = new Vec3(away.x, 0.0D, away.z);
            if (flat.lengthSqr() > 1.0E-4D) {
                flat = flat.normalize();
                player.push(flat.x * 1.3D, 0.55D, flat.z * 1.3D);
                player.hurtMarked = true;
            }
            player.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 100, 0), this);
        }

        int count = Config.particles(80);
        if (count > 0) {
            level.sendParticles(ParticleTypes.PORTAL, this.getX(), this.getY() + 1.0D, this.getZ(),
                    count, 4.0D, 1.0D, 4.0D, 0.5D);
        }
        Fx.ring(level, this.getX(), this.getY() + 0.3D, this.getZ(), 1.5D, ParticleTypes.END_ROD, 40, 0.55D);
        Fx.ring(level, this.getX(), this.getY() + 0.3D, this.getZ(), 1.5D, ParticleTypes.SOUL_FIRE_FLAME, 28, 0.4D);
        Fx.ring(level, this.getX(), this.getY() + 1.4D, this.getZ(), 1.0D, ParticleTypes.REVERSE_PORTAL, 24, 0.3D);
        level.playSound(null, this.getX(), this.getY(), this.getZ(),
                SoundEvents.ENDER_DRAGON_GROWL, SoundSource.HOSTILE, 1.5F, 1.2F);
    }

    private void summonMinions(ServerLevel level) {
        List<PhaseStalker> existing = level.getEntitiesOfClass(PhaseStalker.class, this.getBoundingBox().inflate(24.0D));
        if (existing.size() >= 3) {
            return;
        }
        for (int i = 0; i < 2; i++) {
            BlockPos pos = this.blockPosition().offset(this.random.nextInt(7) - 3, 0, this.random.nextInt(7) - 3);
            PhaseStalker minion = ModEntities.PHASE_STALKER.get().spawn(level, pos, MobSpawnType.MOB_SUMMONED);
            Fx.burst(level, pos.getX() + 0.5D, pos.getY() + 1.0D, pos.getZ() + 0.5D, ParticleTypes.PORTAL, 20, 0.5D, 0.3D);
            if (minion != null && this.getTarget() != null) {
                minion.setTarget(this.getTarget());
            }
        }
    }

    // ------------------------------------------------------------ Hieu ung
    @Override
    public void aiStep() {
        super.aiStep();
        if (this.level().isClientSide) {
            // hai vong hat xoay quanh than; khi nong gian co them lua hon
            double angle = this.tickCount * 0.18D;
            if (Config.roll(this.random, 1)) {
                this.level().addParticle(ParticleTypes.REVERSE_PORTAL,
                        this.getX() + Math.cos(angle) * 1.7D, this.getY() + 0.2D + (this.tickCount % 40) * 0.07D, this.getZ() + Math.sin(angle) * 1.7D,
                        0.0D, 0.02D, 0.0D);
                this.level().addParticle(ParticleTypes.REVERSE_PORTAL,
                        this.getX() - Math.cos(angle) * 1.7D, this.getY() + 0.2D + ((this.tickCount + 20) % 40) * 0.07D, this.getZ() - Math.sin(angle) * 1.7D,
                        0.0D, 0.02D, 0.0D);
            }
            Fx.aura(this, this.getHealth() < this.getMaxHealth() * 0.5F ? ParticleTypes.SOUL_FIRE_FLAME : ParticleTypes.ENCHANT, 3);
        }
    }

    @Override
    public void die(DamageSource source) {
        super.die(source);
        if (this.level() instanceof ServerLevel level) {
            Fx.burst(level, this.getX(), this.getY() + 1.8D, this.getZ(), ParticleTypes.END_ROD, 120, 1.5D, 0.25D);
            Fx.ring(level, this.getX(), this.getY() + 0.3D, this.getZ(), 1.0D, ParticleTypes.SOUL_FIRE_FLAME, 60, 0.8D);
            Fx.ring(level, this.getX(), this.getY() + 1.5D, this.getZ(), 1.0D, ParticleTypes.PORTAL, 60, 0.6D);
        }
    }

    // ------------------------------------------------------------ Thanh mau boss
    @Override
    public void startSeenByPlayer(ServerPlayer player) {
        super.startSeenByPlayer(player);
        this.bossEvent.addPlayer(player);
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        this.bossEvent.removePlayer(player);
    }

    @Override
    public void setCustomName(Component name) {
        super.setCustomName(name);
        this.bossEvent.setName(this.getDisplayName());
    }

    @Override
    public void readAdditionalSaveData(net.minecraft.nbt.CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        if (this.hasCustomName()) {
            this.bossEvent.setName(this.getDisplayName());
        }
    }

    @Override
    public boolean removeWhenFarAway(double distanceToClosestPlayer) {
        return false;
    }

    // ------------------------------------------------------------ Am thanh
    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.ENDERMAN_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.WITHER_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.WITHER_DEATH;
    }
}
