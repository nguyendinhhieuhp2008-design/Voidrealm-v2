package com.voidrealm.mod.item;

import com.voidrealm.mod.effect.Fx;
import com.voidrealm.mod.entity.VoidWisp;
import com.voidrealm.mod.registry.ModEntities;
import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.level.Level;

/** Loi Wisp: chuot phai de goi Void Wisp dong hanh; dung lai de cho no tro ve. */
public class WispCoreItem extends Item {
    public WispCoreItem(Item.Properties properties) {
        super(properties);
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        if (level instanceof ServerLevel server) {
            List<? extends VoidWisp> mine = server.getEntities(ModEntities.VOID_WISP.get(),
                    wisp -> player.getUUID().equals(wisp.getOwnerId()));
            if (!mine.isEmpty()) {
                for (VoidWisp wisp : mine) {
                    Fx.burst(server, wisp.getX(), wisp.getY() + 0.3D, wisp.getZ(), ParticleTypes.REVERSE_PORTAL, 20, 0.3D, 0.2D);
                    wisp.discard();
                }
                player.displayClientMessage(Component.translatable("message.voidrealm.wisp_dismissed"), true);
                level.playSound(null, player.getX(), player.getY(), player.getZ(),
                        SoundEvents.AMETHYST_BLOCK_BREAK, SoundSource.PLAYERS, 0.8F, 0.8F);
            } else {
                VoidWisp wisp = ModEntities.VOID_WISP.get().create(server);
                if (wisp != null) {
                    wisp.moveTo(player.getX(), player.getY() + 1.8D, player.getZ());
                    wisp.setOwner(player);
                    server.addFreshEntity(wisp);
                    Fx.burst(server, wisp.getX(), wisp.getY(), wisp.getZ(), ParticleTypes.END_ROD, 24, 0.4D, 0.15D);
                    player.displayClientMessage(Component.translatable("message.voidrealm.wisp_summoned"), true);
                    level.playSound(null, player.getX(), player.getY(), player.getZ(),
                            SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.PLAYERS, 1.0F, 1.2F);
                }
            }
        }
        player.getCooldowns().addCooldown(this, 40);
        return InteractionResultHolder.sidedSuccess(stack, level.isClientSide());
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return true;
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidrealm.wisp_core").withStyle(ChatFormatting.AQUA));
    }
}
