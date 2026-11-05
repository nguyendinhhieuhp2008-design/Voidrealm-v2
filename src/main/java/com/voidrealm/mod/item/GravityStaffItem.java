package com.voidrealm.mod.item;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.effect.Fx;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Truong Trong Luc: chuot phai de keo moi quai vat xung quanh ve phia ban va lam cham chung.
 */
public class GravityStaffItem extends Item {
    public GravityStaffItem(Item.Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.getCooldowns().isOnCooldown(this)) {
            return InteractionResultHolder.pass(stack);
        }

        if (!level.isClientSide) {
            double radius = Config.GRAVITY_RADIUS.get();
            AABB area = player.getBoundingBox().inflate(radius);
            List<Mob> targets = level.getEntitiesOfClass(Mob.class, area, mob -> mob.isAlive());
            for (Mob mob : targets) {
                Vec3 pull = player.position().subtract(mob.position());
                if (pull.lengthSqr() < 1.0E-3D) {
                    continue;
                }
                Vec3 motion = pull.normalize().scale(1.1D).add(0.0D, 0.25D, 0.0D);
                mob.setDeltaMovement(motion);
                mob.hurtMarked = true;
                mob.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1), player);
                if (level instanceof ServerLevel fxLevel) {
                    Fx.burst(fxLevel, mob.getX(), mob.getY() + mob.getBbHeight() * 0.5D, mob.getZ(), ParticleTypes.REVERSE_PORTAL, 5, 0.3D, 0.1D);
                }
            }

            if (level instanceof ServerLevel serverLevel) {
                int count = Config.particles(50);
                if (count > 0) {
                    serverLevel.sendParticles(ParticleTypes.REVERSE_PORTAL,
                            player.getX(), player.getY() + 1.0D, player.getZ(), count, radius / 3.0D, 0.8D, radius / 3.0D, 0.15D);
                }
            }
            if (level instanceof ServerLevel ringLevel) {
                Fx.ring(ringLevel, player.getX(), player.getY() + 0.2D, player.getZ(), radius, ParticleTypes.END_ROD, 36, -0.35D);
                Fx.ring(ringLevel, player.getX(), player.getY() + 1.0D, player.getZ(), radius * 0.6D, ParticleTypes.REVERSE_PORTAL, 24, -0.25D);
            }
            level.playSound(null, player.getX(), player.getY(), player.getZ(),
                    SoundEvents.ENDERMAN_STARE, SoundSource.PLAYERS, 0.8F, 1.4F);
            stack.hurtAndBreak(2, player, LivingEntity.getSlotForHand(hand));
        }

        player.getCooldowns().addCooldown(this, Config.GRAVITY_COOLDOWN_TICKS.get());
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return true;
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidrealm.gravity_staff").withStyle(ChatFormatting.DARK_PURPLE));
    }
}
