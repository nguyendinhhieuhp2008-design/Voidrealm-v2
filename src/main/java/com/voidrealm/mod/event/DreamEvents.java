package com.voidrealm.mod.event;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.registry.ModItems;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.AbstractArrow;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.common.damagesource.DamageContainer;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.level.BlockEvent;
import com.voidrealm.mod.item.DreamDrillItem;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;

/** Riu chien Mong Tinh xuyen giap; no Mong Tinh ban ten manh + xuyen. */
@EventBusSubscriber(modid = VoidRealm.MODID)
public class DreamEvents {

    @SubscribeEvent
    public static void onIncomingDamage(LivingIncomingDamageEvent event) {
        if (event.getSource().getDirectEntity() instanceof LivingEntity attacker
                && event.getSource().getEntity() == attacker
                && attacker.getMainHandItem().is(ModItems.DREAM_BATTLE_AXE.get())) {
            event.addReductionModifier(DamageContainer.Reduction.ARMOR, (container, reduction) -> 0.0F);
        }
    }

    @SubscribeEvent
    public static void onBlockBreak(BlockEvent.BreakEvent event) {
        if (event.getPlayer().getMainHandItem().getItem() instanceof DreamDrillItem) {
            DreamDrillItem.breakArea(event.getPlayer().getMainHandItem(), event.getPos(), event.getPlayer());
        }
    }

    @SubscribeEvent
    public static void onArrowJoin(EntityJoinLevelEvent event) {
        if (event.getLevel().isClientSide() || !(event.getEntity() instanceof AbstractArrow arrow)
                || !(arrow.getOwner() instanceof LivingEntity owner) || arrow.getTags().contains("voidrealm_dream")) {
            return;
        }
        if (owner.getMainHandItem().is(ModItems.DREAM_CROSSBOW.get()) || owner.getOffhandItem().is(ModItems.DREAM_CROSSBOW.get())) {
            arrow.addTag("voidrealm_dream");
            arrow.setBaseDamage(arrow.getBaseDamage() + 7.0D);
            arrow.setGlowingTag(true);
        }
    }

    private DreamEvents() {
    }
}
