package com.voidrealm.mod.entity;

import com.voidrealm.mod.effect.Fx;
import java.util.EnumSet;
import java.util.List;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.control.FlyingMoveControl;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomFlyingGoal;
import net.minecraft.world.entity.ai.navigation.FlyingPathNavigation;
import net.minecraft.world.entity.ai.navigation.PathNavigation;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.LightBlock;
import net.minecraft.world.phys.Vec3;

/**
 * Void Wisp: sinh vat dong hanh bay quanh chu nhan, toa sang (dat khoi anh sang ao) va
 * tu nhat vat pham dang roi xuong vuc ve phia chu nhan.
 */
public class VoidWisp extends PathfinderMob {
    private UUID ownerId;
    private BlockPos lightPos;

    public VoidWisp(EntityType<? extends VoidWisp> type, Level level) {
        super(type, level);
        this.moveControl = new FlyingMoveControl(this, 20, true);
        this.setNoGravity(true);
        this.xpReward = 0;
    }

    public static AttributeSupplier.Builder createAttributes() {
        return Mob.createMobAttributes()
                .add(Attributes.MAX_HEALTH, 12.0D)
                .add(Attributes.FLYING_SPEED, 0.7D)
                .add(Attributes.MOVEMENT_SPEED, 0.35D)
                .add(Attributes.FOLLOW_RANGE, 32.0D);
    }

    public UUID getOwnerId() {
        return this.ownerId;
    }

    public void setOwner(Player owner) {
        this.ownerId = owner.getUUID();
    }

    private Player owner() {
        return this.ownerId == null ? null : this.level().getPlayerByUUID(this.ownerId);
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
        this.goalSelector.addGoal(1, new FollowOwnerGoal());
        this.goalSelector.addGoal(5, new WaterAvoidingRandomFlyingGoal(this, 1.0D));
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        return source.is(DamageTypeTags.BYPASSES_INVULNERABILITY) && super.hurt(source, amount);
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
        return SoundEvents.AMETHYST_BLOCK_CHIME;
    }

    @Override
    public int getAmbientSoundInterval() {
        return 220;
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (this.level().isClientSide) {
            Fx.aura(this, ParticleTypes.END_ROD, 4);
            Fx.aura(this, ParticleTypes.REVERSE_PORTAL, 5);
            return;
        }
        // tu gan chu nhan neu chua co (trung sinh bang trung)
        if (this.ownerId == null && this.tickCount % 40 == 0) {
            Player nearest = this.level().getNearestPlayer(this, 8.0D);
            if (nearest != null) {
                this.ownerId = nearest.getUUID();
            }
        }
        Player owner = owner();
        if (owner != null && this.tickCount % 5 == 0) {
            collectFallingItems(owner);
        }
        if (this.tickCount % 4 == 0) {
            updateLight();
        }
    }

    private void collectFallingItems(Player owner) {
        double minY = this.level().getMinBuildHeight() + 24.0D;
        List<ItemEntity> items = this.level().getEntitiesOfClass(ItemEntity.class,
                owner.getBoundingBox().inflate(20.0D, 48.0D, 20.0D),
                item -> item.isAlive() && !item.onGround() && item.getDeltaMovement().y < -0.2D
                        && (item.getY() < owner.getY() - 5.0D || item.getY() < minY));
        for (ItemEntity item : items) {
            if (this.level() instanceof ServerLevel server) {
                Fx.burst(server, item.getX(), item.getY(), item.getZ(), ParticleTypes.REVERSE_PORTAL, 10, 0.2D, 0.1D);
            }
            item.setDeltaMovement(Vec3.ZERO);
            item.moveTo(owner.getX(), owner.getY() + 0.6D, owner.getZ());
            item.setNoPickUpDelay();
            if (this.level() instanceof ServerLevel server) {
                Fx.burst(server, owner.getX(), owner.getY() + 0.8D, owner.getZ(), ParticleTypes.END_ROD, 8, 0.3D, 0.05D);
            }
            this.playSound(SoundEvents.AMETHYST_BLOCK_RESONATE, 0.8F, 1.4F);
        }
    }

    private void updateLight() {
        BlockPos pos = this.blockPosition();
        if (pos.equals(this.lightPos)) {
            return;
        }
        clearLight();
        if (this.level().getBlockState(pos).isAir()) {
            this.level().setBlock(pos, Blocks.LIGHT.defaultBlockState().setValue(LightBlock.LEVEL, 12), 2);
            this.lightPos = pos;
        }
    }

    private void clearLight() {
        if (this.lightPos != null) {
            if (this.level().getBlockState(this.lightPos).is(Blocks.LIGHT)) {
                this.level().setBlock(this.lightPos, Blocks.AIR.defaultBlockState(), 2);
            }
            this.lightPos = null;
        }
    }

    @Override
    public void remove(RemovalReason reason) {
        if (!this.level().isClientSide) {
            clearLight();
        }
        super.remove(reason);
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

    /** Bay theo chu nhan, quanh quan tren dau khi o gan. */
    private class FollowOwnerGoal extends Goal {
        FollowOwnerGoal() {
            this.setFlags(EnumSet.of(Goal.Flag.MOVE));
        }

        @Override
        public boolean canUse() {
            return owner() != null;
        }

        @Override
        public void tick() {
            Player owner = owner();
            if (owner == null) {
                return;
            }
            double distSqr = VoidWisp.this.distanceToSqr(owner);
            if (distSqr > 26.0D * 26.0D) {
                VoidWisp.this.moveTo(owner.getX(), owner.getY() + 1.8D, owner.getZ());
                VoidWisp.this.getNavigation().stop();
                return;
            }
            double t = VoidWisp.this.tickCount * 0.06D;
            double tx;
            double ty;
            double tz;
            if (distSqr > 25.0D) {
                tx = owner.getX();
                ty = owner.getY() + 1.9D;
                tz = owner.getZ();
            } else {
                tx = owner.getX() + Math.cos(t) * 1.5D;
                ty = owner.getY() + 1.9D + Math.sin(t * 1.7D) * 0.25D;
                tz = owner.getZ() + Math.sin(t) * 1.5D;
            }
            VoidWisp.this.getMoveControl().setWantedPosition(tx, ty, tz, distSqr > 25.0D ? 1.6D : 1.0D);
            VoidWisp.this.getLookControl().setLookAt(owner);
        }
    }
}
