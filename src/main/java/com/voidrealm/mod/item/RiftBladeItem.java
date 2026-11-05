package com.voidrealm.mod.item;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.effect.Fx;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Kiem Xe Khong Gian: chuot phai de "chop" (dich chuyen) mot doan ngan ve phia truoc.
 */
public class RiftBladeItem extends SwordItem {
    public RiftBladeItem(Tier tier, Item.Properties properties) {
        super(tier, properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.getCooldowns().isOnCooldown(this)) {
            return InteractionResultHolder.pass(stack);
        }

        Vec3 look = player.getLookAngle();
        Vec3 dir = new Vec3(look.x, 0.0D, look.z);
        if (dir.lengthSqr() < 1.0E-4D) {
            return InteractionResultHolder.pass(stack);
        }
        dir = dir.normalize();

        double best = 0.0D;
        double max = Config.BLINK_RANGE.get();
        for (double d = 0.5D; d <= max; d += 0.5D) {
            AABB moved = player.getBoundingBox().move(dir.scale(d));
            if (level.noCollision(player, moved)) {
                best = d;
            } else {
                break;
            }
        }
        if (best < 1.0D) {
            return InteractionResultHolder.fail(stack);
        }

        if (!level.isClientSide && player instanceof ServerPlayer serverPlayer) {
            Vec3 from = serverPlayer.position();
            double nx = from.x + dir.x * best;
            double ny = from.y;
            double nz = from.z + dir.z * best;

            if (level instanceof ServerLevel serverLevel) {
                int count = Config.particles(30);
                if (count > 0) {
                    serverLevel.sendParticles(ParticleTypes.PORTAL, from.x, from.y + 1.0D, from.z, count, 0.3D, 0.6D, 0.3D, 0.2D);
                    serverLevel.sendParticles(ParticleTypes.PORTAL, nx, ny + 1.0D, nz, count, 0.3D, 0.6D, 0.3D, 0.2D);
                }
                Fx.line(serverLevel, new Vec3(from.x, from.y + 1.0D, from.z), new Vec3(nx, ny + 1.0D, nz), ParticleTypes.END_ROD, 0.4D);
                Fx.line(serverLevel, new Vec3(from.x, from.y + 0.5D, from.z), new Vec3(nx, ny + 0.5D, nz), ParticleTypes.REVERSE_PORTAL, 0.5D);
            }
            level.playSound(null, from.x, from.y, from.z, SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 1.0F, 1.2F);
            serverPlayer.connection.teleport(nx, ny, nz, serverPlayer.getYRot(), serverPlayer.getXRot());
            serverPlayer.fallDistance = 0.0F;
            level.playSound(null, nx, ny, nz, SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 1.0F, 1.0F);
            stack.hurtAndBreak(6, serverPlayer, LivingEntity.getSlotForHand(hand));
        }

        player.getCooldowns().addCooldown(this, Config.BLINK_COOLDOWN_TICKS.get());
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return true;
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidrealm.rift_blade").withStyle(ChatFormatting.DARK_PURPLE));
    }
}
