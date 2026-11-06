package com.voidrealm.mod.event;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.effect.Fx;
import com.voidrealm.mod.item.VoidTetherItem;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

/** Quan ly co che du day (grappling) cua Day Thung Trong Luc. Chi chay tren may chu. */
@EventBusSubscriber(modid = VoidRealm.MODID)
public class TetherManager {
    private static final int MAX_TICKS = 140;
    private static final Map<UUID, Tether> ACTIVE = new HashMap<>();

    private static class Tether {
        final Vec3 anchor;
        int ticks;

        Tether(Vec3 anchor) {
            this.anchor = anchor;
        }
    }

    public static boolean isAttached(Player player) {
        return ACTIVE.containsKey(player.getUUID());
    }

    public static void attach(Player player, Vec3 anchor) {
        ACTIVE.put(player.getUUID(), new Tether(anchor));
        Vec3 motion = player.getDeltaMovement();
        player.setDeltaMovement(motion.x, Math.max(motion.y, 0.35D), motion.z);
        player.hurtMarked = true;
    }

    public static void release(Player player) {
        Tether tether = ACTIVE.remove(player.getUUID());
        if (tether == null) {
            return;
        }
        player.resetFallDistance();
        player.addEffect(new MobEffectInstance(MobEffects.SLOW_FALLING, 100, 0, true, false, true));
        if (player.level() instanceof ServerLevel level) {
            Fx.burst(level, tether.anchor.x, tether.anchor.y, tether.anchor.z, ParticleTypes.END_ROD, 10, 0.2D, 0.05D);
            level.playSound(null, player.getX(), player.getY(), player.getZ(),
                    SoundEvents.CHAIN_BREAK, SoundSource.PLAYERS, 0.7F, 1.4F);
        }
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        Player player = event.getEntity();
        if (player.level().isClientSide) {
            return;
        }
        Tether tether = ACTIVE.get(player.getUUID());
        if (tether == null) {
            return;
        }
        tether.ticks++;
        boolean holding = player.getMainHandItem().getItem() instanceof VoidTetherItem
                || player.getOffhandItem().getItem() instanceof VoidTetherItem;
        Vec3 body = player.position().add(0.0D, player.getBbHeight() * 0.6D, 0.0D);
        Vec3 to = tether.anchor.subtract(body);
        double dist = to.length();

        if (!player.isAlive() || !holding || tether.ticks > MAX_TICKS || dist < 2.2D
                || (player.isShiftKeyDown() && tether.ticks > 4)) {
            release(player);
            return;
        }

        Vec3 dir = to.scale(1.0D / dist);
        Vec3 motion = player.getDeltaMovement().scale(0.93D).add(dir.scale(0.17D));
        if (motion.length() > 1.35D) {
            motion = motion.normalize().scale(1.35D);
        }
        player.setDeltaMovement(motion);
        player.hurtMarked = true;
        player.resetFallDistance();

        if (tether.ticks % 3 == 0 && player.level() instanceof ServerLevel level) {
            Vec3 hand = player.getEyePosition().add(player.getLookAngle().scale(0.5D)).add(0.0D, -0.3D, 0.0D);
            Fx.line(level, hand, tether.anchor, ParticleTypes.END_ROD, 1.0D);
        }
    }

    @SubscribeEvent
    public static void onLogout(PlayerEvent.PlayerLoggedOutEvent event) {
        ACTIVE.remove(event.getEntity().getUUID());
    }

    private TetherManager() {
    }
}
