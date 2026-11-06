package com.voidrealm.mod.item;

import com.voidrealm.mod.entity.BlackHole;
import com.voidrealm.mod.registry.ModEntities;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/** Truong Bop Me Khong Gian: chuot phai tao lo den hut quai vat tai diem ngam. */
public class WarpRodItem extends Item {
    public WarpRodItem(Item.Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (player.getCooldowns().isOnCooldown(this)) {
            return InteractionResultHolder.pass(stack);
        }
        if (!level.isClientSide) {
            HitResult hit = player.pick(24.0D, 1.0F, false);
            Vec3 target = hit.getType() == HitResult.Type.MISS
                    ? player.getEyePosition().add(player.getLookAngle().scale(10.0D))
                    : hit.getLocation();
            // dat lo den cao hon mat dat mot chut
            BlackHole hole = ModEntities.BLACK_HOLE.get().create(level);
            if (hole != null) {
                hole.moveTo(target.x, target.y + 1.2D, target.z);
                hole.setOwner(player);
                level.addFreshEntity(hole);
            }
            level.playSound(null, player.getX(), player.getY(), player.getZ(),
                    SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 0.9F, 0.5F);
            stack.hurtAndBreak(3, player, LivingEntity.getSlotForHand(hand));
        }
        player.getCooldowns().addCooldown(this, 220);
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return true;
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidrealm.warp_rod").withStyle(ChatFormatting.DARK_PURPLE));
    }
}
