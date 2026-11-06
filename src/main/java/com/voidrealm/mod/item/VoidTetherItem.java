package com.voidrealm.mod.item;

import com.voidrealm.mod.event.TetherManager;
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

/** Day Thung Trong Luc: chuot phai ban moc vao khoi, tu keo ban ve phia do (du day). Nhan Shift de tha. */
public class VoidTetherItem extends Item {
    public static final double RANGE = 36.0D;

    public VoidTetherItem(Item.Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (!level.isClientSide) {
            if (TetherManager.isAttached(player)) {
                TetherManager.release(player);
                return InteractionResultHolder.success(stack);
            }
            if (player.getCooldowns().isOnCooldown(this)) {
                return InteractionResultHolder.pass(stack);
            }
            HitResult hit = player.pick(RANGE, 1.0F, false);
            if (hit.getType() == HitResult.Type.BLOCK) {
                TetherManager.attach(player, hit.getLocation());
                level.playSound(null, player.getX(), player.getY(), player.getZ(),
                        SoundEvents.CROSSBOW_SHOOT, SoundSource.PLAYERS, 0.8F, 1.6F);
                stack.hurtAndBreak(1, player, LivingEntity.getSlotForHand(hand));
            } else {
                player.displayClientMessage(Component.translatable("message.voidrealm.tether_miss"), true);
                player.getCooldowns().addCooldown(this, 10);
            }
        }
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidrealm.void_tether").withStyle(ChatFormatting.DARK_PURPLE));
    }
}
