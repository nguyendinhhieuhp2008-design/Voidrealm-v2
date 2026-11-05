package com.voidrealm.mod.item;

import com.voidrealm.mod.effect.Fx;
import java.util.List;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;

/**
 * Luoi Hai Hu Vo: danh trung gay Heo Hon (Wither) va hut mot it mau cho nguoi cam.
 */
public class VoidReaperItem extends SwordItem {
    public VoidReaperItem(Tier tier, Item.Properties properties) {
        super(tier, properties);
    }

    @Override
    public boolean hurtEnemy(ItemStack stack, LivingEntity target, LivingEntity attacker) {
        target.addEffect(new MobEffectInstance(MobEffects.WITHER, 80, 0), attacker);
        attacker.heal(1.0F);
        if (target.level() instanceof ServerLevel level) {
            double y = target.getY() + target.getBbHeight() * 0.5D;
            Fx.burst(level, target.getX(), y, target.getZ(), ParticleTypes.SCULK_SOUL, 6, 0.3D, 0.05D);
            Fx.burst(level, target.getX(), y, target.getZ(), ParticleTypes.SOUL_FIRE_FLAME, 8, 0.35D, 0.04D);
            Fx.burst(level, attacker.getX(), attacker.getY() + 1.0D, attacker.getZ(), ParticleTypes.SOUL, 3, 0.3D, 0.03D);
        }
        return super.hurtEnemy(stack, target, attacker);
    }

    @Override
    public boolean isFoil(ItemStack stack) {
        return true;
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("tooltip.voidrealm.void_reaper").withStyle(ChatFormatting.DARK_PURPLE));
    }
}
