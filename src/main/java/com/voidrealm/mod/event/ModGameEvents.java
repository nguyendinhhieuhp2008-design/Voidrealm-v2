package com.voidrealm.mod.event;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.effect.Fx;
import com.voidrealm.mod.registry.ModArmorMaterials;
import com.voidrealm.mod.registry.ModItems;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.ArmorMaterial;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.minecraft.tags.DamageTypeTags;
import net.neoforged.neoforge.event.entity.living.LivingFallEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;
import net.neoforged.neoforge.registries.DeferredHolder;

/** Hieu ung khi mac du bo giap. Chi chay moi 1 giay tren may chu de nhe may. */
@EventBusSubscriber(modid = VoidRealm.MODID)
public class ModGameEvents {

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        Player player = event.getEntity();
        if (player.level().isClientSide || player.tickCount % 10 != 0 || !Config.ARMOR_SET_BONUS.get()) {
            return;
        }
        boolean applyEffects = player.tickCount % 20 == 0;
        applyEyeOfTheVoid(player);

        if (wearsFullSet(player, ModArmorMaterials.VOID_STEEL)) {
            if (applyEffects) {
                player.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 60, 0, true, false, true));
                player.addEffect(new MobEffectInstance(MobEffects.FIRE_RESISTANCE, 60, 0, true, false, true));
            }
            if (player.level() instanceof ServerLevel level) {
                Fx.burst(level, player.getX(), player.getY() + 1.0D, player.getZ(), ParticleTypes.END_ROD, 2, 0.45D, 0.01D);
            }
        }

        if (wearsFullSet(player, ModArmorMaterials.PHASE_CLOTH)) {
            if (applyEffects) {
                player.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 60, 0, true, false, true));
                player.addEffect(new MobEffectInstance(MobEffects.JUMP, 60, 0, true, false, true));
            }
            if (player.level() instanceof ServerLevel level) {
                Fx.burst(level, player.getX(), player.getY() + 0.9D, player.getZ(), ParticleTypes.REVERSE_PORTAL, 3, 0.4D, 0.02D);
            }
        }
    }

    /** Mat Nhin Thuc Tai: lam moi sinh vat (ke ca tang hinh) quanh nguoi cam phat sang xuyen tuong. */
    private static void applyEyeOfTheVoid(Player player) {
        if (!player.getMainHandItem().is(ModItems.EYE_OF_THE_VOID.get())
                && !player.getOffhandItem().is(ModItems.EYE_OF_THE_VOID.get())) {
            return;
        }
        for (LivingEntity target : player.level().getEntitiesOfClass(LivingEntity.class,
                player.getBoundingBox().inflate(24.0D), e -> e != player && e.isAlive())) {
            target.addEffect(new MobEffectInstance(MobEffects.GLOWING, 30, 0, true, false, false));
        }
    }

    /** Bo Hu Anh: khong nhan sat thuong khi roi. */
    @SubscribeEvent
    public static void onFall(LivingFallEvent event) {
        if (event.getEntity() instanceof Player player && Config.ARMOR_SET_BONUS.get()
                && wearsFullSet(player, ModArmorMaterials.PHASE_CLOTH)) {
            event.setDamageMultiplier(0.0F);
        }
    }

    /** Bo Thep Hu Khong: giam 50% sat thuong no. */
    @SubscribeEvent
    public static void onIncomingDamage(LivingIncomingDamageEvent event) {
        if (event.getEntity() instanceof Player player && Config.ARMOR_SET_BONUS.get()
                && event.getSource().is(DamageTypeTags.IS_EXPLOSION)
                && wearsFullSet(player, ModArmorMaterials.VOID_STEEL)) {
            event.setAmount(event.getAmount() * 0.5F);
        }
    }

    private static boolean wearsFullSet(Player player, DeferredHolder<ArmorMaterial, ArmorMaterial> material) {
        for (ItemStack stack : player.getArmorSlots()) {
            if (!(stack.getItem() instanceof ArmorItem armor) || armor.getMaterial().value() != material.get()) {
                return false;
            }
        }
        return true;
    }

    private ModGameEvents() {
    }
}
