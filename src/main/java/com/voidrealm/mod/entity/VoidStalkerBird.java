package com.voidrealm.mod.entity;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.effect.Fx;
import com.voidrealm.mod.registry.ModItems;
import java.util.UUID;
import javax.annotation.Nullable;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MoverType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.control.FlyingMoveControl;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomFlyingGoal;
import net.minecraft.world.entity.ai.navigation.FlyingPathNavigation;
import net.minecraft.world.entity.ai.navigation.PathNavigation;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Void Stalker Bird: chim khong lo bay duoc, co the thuan hoa (cho an Tao/Banh Hu Khong) va cuoi.
 * Khi cuoi: nhin len/xuong de bay len/xuong, nhan W de lao toi, Shift de xuong ngua.
 */
public class VoidStalkerBird extends PathfinderMob {
    private UUID ownerId;

    public VoidStalkerBird(EntityType<? extends VoidStalkerBird> type, Level level) {
        super(type, level);
        this.moveControl = new FlyingMoveControl(this, 20, true);
        this.setNoGravity(true);
        this.xpReward = 5;
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 30.0D)
                .add(Attributes.MOVEMENT_SPEED, 0.35D)
                .add(Attributes.FLYING_SPEED, 0.8D)
                .add(Attributes.FOLLOW_RANGE, 32.0D);
    }

    public boolean isTame() {
        return this.ownerId != null;
    }

    @Override
    protected PathNavigation createNavigation(Level level) {
        FlyingPathNavigation navigation = new FlyingPathNavigation(this, level);
        navigation.setCanOpenDoors(false);
        navigation.setCanFloat(true);
        navigation.setCanPassDoors(true);
        return navigation;
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(5, new WaterAvoidingRandomFlyingGoal(this, 1.0D));
        this.goalSelector.addGoal(6, new LookAtPlayerGoal(this, Player.class, 8.0F));
        this.goalSelector.addGoal(7, new RandomLookAroundGoal(this));
    }

    @Override
    public boolean causeFallDamage(float fallDistance, float multiplier, DamageSource source) {
        return false;
    }

    @Override
    public boolean removeWhenFarAway(double distanceToClosestPlayer) {
        return false;
    }

    @Override
    protected SoundEvent getAmbientSound() {
        return SoundEvents.PARROT_AMBIENT;
    }

    @Override
    protected SoundEvent getHurtSound(DamageSource source) {
        return SoundEvents.PARROT_HURT;
    }

    @Override
    protected SoundEvent getDeathSound() {
        return SoundEvents.PARROT_DEATH;
    }

    @Override
    public InteractionResult mobInteract(Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!this.isTame()) {
            if (stack.is(ModItems.VOID_APPLE.get()) || stack.is(ModItems.VOID_FRUIT.get())) {
                if (!this.level().isClientSide) {
                    stack.consume(1, player);
                    if (this.random.nextInt(3) == 0) {
                        this.ownerId = player.getUUID();
                        this.setPersistenceRequired();
                        this.setHealth(this.getMaxHealth());
                        if (this.level() instanceof ServerLevel server) {
                            server.sendParticles(ParticleTypes.HEART, this.getX(), this.getY() + this.getBbHeight(),
                                    this.getZ(), 8, 0.5D, 0.5D, 0.5D, 0.02D);
                        }
                    } else if (this.level() instanceof ServerLevel server) {
                        server.sendParticles(ParticleTypes.SMOKE, this.getX(), this.getY() + this.getBbHeight() * 0.7D,
                                this.getZ(), 6, 0.4D, 0.4D, 0.4D, 0.02D);
                    }
                }
                return InteractionResult.sidedSuccess(this.level().isClientSide);
            }
            return super.mobInteract(player, hand);
        }
        if (player.getUUID().equals(this.ownerId) && !player.isSecondaryUseActive()) {
            if (!this.level().isClientSide) {
                player.startRiding(this);
            }
            return InteractionResult.sidedSuccess(this.level().isClientSide);
        }
        return super.mobInteract(player, hand);
    }

    @Nullable
    @Override
    public LivingEntity getControllingPassenger() {
        return this.getFirstPassenger() instanceof Player player ? player : null;
    }

    @Override
    public void travel(Vec3 input) {
        LivingEntity rider = this.getControllingPassenger();
        if (this.isAlive() && this.isVehicle() && rider != null) {
            this.setYRot(rider.getYRot());
            this.yRotO = this.getYRot();
            this.setXRot(rider.getXRot() * 0.5F);
            this.setRot(this.getYRot(), this.getXRot());
            this.yBodyRot = this.getYRot();
            this.yHeadRot = this.yBodyRot;
            if (this.isControlledByLocalInstance()) {
                float forward = rider.zza;
                Vec3 look = rider.getLookAngle();
                Vec3 target = forward > 0.0F ? look.scale(0.95D)
                        : forward < 0.0F ? look.scale(-0.3D) : Vec3.ZERO;
                Vec3 motion = this.getDeltaMovement().lerp(target, 0.12D);
                if (rider.isShiftKeyDown() && forward == 0.0F) {
                    motion = motion.add(0.0D, -0.06D, 0.0D);
                }
                this.setDeltaMovement(motion);
                this.move(MoverType.SELF, this.getDeltaMovement());
            } else {
                this.setDeltaMovement(Vec3.ZERO);
            }
            this.calculateEntityAnimation(false);
        } else {
            super.travel(input);
        }
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (this.level().isClientSide) {
            if (this.isVehicle()) {
                Fx.aura(this, ParticleTypes.REVERSE_PORTAL, 3);
            }
            Fx.aura(this, ParticleTypes.END_ROD, 12);
        }
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        if (this.ownerId != null) {
            tag.putUUID("Owner", this.ownerId);
        }
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        if (tag.hasUUID("Owner")) {
            this.ownerId = tag.getUUID("Owner");
        }
    }
}
