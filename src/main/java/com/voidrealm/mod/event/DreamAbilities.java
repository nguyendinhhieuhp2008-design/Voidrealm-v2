package com.voidrealm.mod.event;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.item.DreamArmor;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import net.minecraft.network.chat.Component;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.TamableAnimal;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.tick.ServerTickEvent;
import org.joml.Vector3f;

/** Ky nang bo giap Mong Tinh: C = tang toc (nhu phao hoa) khi dang luot, K = xuc tu xanh quanh 8 block. */
@EventBusSubscriber(modid = VoidRealm.MODID)
public class DreamAbilities {
    private static final double RANGE = 8.0D;
    private static final DustParticleOptions BLUE = new DustParticleOptions(new Vector3f(0.15F, 0.5F, 1.0F), 1.5F);
    private static final DustParticleOptions CYAN = new DustParticleOptions(new Vector3f(0.6F, 0.95F, 1.0F), 1.0F);
    private static final Map<UUID, Integer> BOOSTING = new HashMap<>();
    private static final List<Tentacle> TENTACLES = new ArrayList<>();

    private static final class Tentacle {
        final ServerPlayer owner;
        final LivingEntity target;
        final double phase;
        final boolean primary;
        int age;

        Tentacle(ServerPlayer owner, LivingEntity target, double phase, boolean primary) {
            this.owner = owner;
            this.target = target;
            this.phase = phase;
            this.primary = primary;
        }
    }

    private static boolean ready(ServerPlayer player, String key, int cooldown) {
        long now = player.level().getGameTime();
        long until = player.getPersistentData().getLong(key);
        if (now < until) {
            return false;
        }
        player.getPersistentData().putLong(key, now + cooldown);
        return true;
    }

    public static void boost(ServerPlayer player) {
        if (!DreamArmor.hasFullSet(player)) {
            player.displayClientMessage(Component.translatable("message.voidrealm.dream_need_set"), true);
            return;
        }
        if (!player.isFallFlying()) {
            player.displayClientMessage(Component.translatable("message.voidrealm.dream_need_flight"), true);
            return;
        }
        if (!ready(player, "voidrealm_dream_boost", 30)) {
            return;
        }
        BOOSTING.put(player.getUUID(), 14);
        player.getItemBySlot(EquipmentSlot.CHEST).hurtAndBreak(2, player, EquipmentSlot.CHEST);
        player.level().playSound(null, player.blockPosition(), SoundEvents.FIREWORK_ROCKET_LAUNCH, SoundSource.PLAYERS, 1.0F, 0.9F);
    }

    public static void tentacles(ServerPlayer player) {
        if (!DreamArmor.hasFullSet(player)) {
            player.displayClientMessage(Component.translatable("message.voidrealm.dream_need_set"), true);
            return;
        }
        ServerLevel level = player.serverLevel();
        List<LivingEntity> targets = new ArrayList<>(level.getEntitiesOfClass(LivingEntity.class,
                player.getBoundingBox().inflate(RANGE), e -> e != player && e.isAlive() && e.distanceToSqr(player) <= RANGE * RANGE
                        && (e instanceof Enemy || (e instanceof Mob m && m.getTarget() == player))
                        && !(e instanceof TamableAnimal t && t.isTame())));
        if (targets.isEmpty()) {
            player.displayClientMessage(Component.translatable("message.voidrealm.dream_no_target"), true);
            return;
        }
        if (!ready(player, "voidrealm_dream_tentacle", 60)) {
            return;
        }
        targets.sort(Comparator.comparingDouble(e -> e.distanceToSqr(player)));
        if (targets.size() > 6) {
            targets = targets.subList(0, 6);
        }
        for (LivingEntity target : targets) {
            for (int k = 0; k < 3; k++) {
                TENTACLES.add(new Tentacle(player, target, k * 2.1D + level.random.nextDouble(), k == 0));
            }
        }
        player.getItemBySlot(EquipmentSlot.CHEST).hurtAndBreak(2, player, EquipmentSlot.CHEST);
        level.playSound(null, player.blockPosition(), SoundEvents.SCULK_CLICKING, SoundSource.PLAYERS, 1.2F, 0.6F);
        level.playSound(null, player.blockPosition(), SoundEvents.ELDER_GUARDIAN_CURSE, SoundSource.PLAYERS, 0.4F, 1.6F);
    }

    @SubscribeEvent
    public static void onServerTick(ServerTickEvent.Post event) {
        Iterator<Map.Entry<UUID, Integer>> it = BOOSTING.entrySet().iterator();
        while (it.hasNext()) {
            Map.Entry<UUID, Integer> e = it.next();
            ServerPlayer p = event.getServer().getPlayerList().getPlayer(e.getKey());
            if (p == null || !p.isFallFlying() || e.getValue() <= 0) {
                it.remove();
                continue;
            }
            Vec3 look = p.getLookAngle();
            Vec3 v = p.getDeltaMovement();
            p.setDeltaMovement(v.add(look.x * 0.1D + (look.x * 1.5D - v.x) * 0.5D,
                    look.y * 0.1D + (look.y * 1.5D - v.y) * 0.5D,
                    look.z * 0.1D + (look.z * 1.5D - v.z) * 0.5D));
            p.hurtMarked = true;
            p.serverLevel().sendParticles(ParticleTypes.FIREWORK, p.getX() - look.x, p.getY() + 0.5D - look.y, p.getZ() - look.z,
                    3, 0.1D, 0.1D, 0.1D, 0.02D);
            p.serverLevel().sendParticles(BLUE, p.getX() - look.x, p.getY() + 0.5D, p.getZ() - look.z, 4, 0.2D, 0.2D, 0.2D, 0.0D);
            e.setValue(e.getValue() - 1);
        }

        Iterator<Tentacle> ti = TENTACLES.iterator();
        while (ti.hasNext()) {
            Tentacle t = ti.next();
            if (!t.owner.isAlive() || !t.target.isAlive() || t.owner.hasDisconnected() || t.age > 12) {
                ti.remove();
                continue;
            }
            ServerLevel level = t.owner.serverLevel();
            if (t.target.level() != level) {
                ti.remove();
                continue;
            }
            Vec3 start = new Vec3(t.owner.getX(), t.owner.getY() + 1.1D, t.owner.getZ());
            Vec3 end = new Vec3(t.target.getX(), t.target.getY() + t.target.getBbHeight() * 0.5D, t.target.getZ());
            Vec3 dir = end.subtract(start);
            double len = dir.length();
            if (len > 0.01D) {
                Vec3 d = dir.scale(1.0D / len);
                Vec3 u = d.cross(new Vec3(0.0D, 1.0D, 0.0D));
                if (u.lengthSqr() < 1.0E-4D) {
                    u = new Vec3(1.0D, 0.0D, 0.0D);
                }
                u = u.normalize();
                Vec3 w = d.cross(u).normalize();
                double progress = Math.min(1.0D, (t.age + 1) / 7.0D);
                int steps = (int) (len * 3.0D * progress) + 1;
                for (int i = 0; i <= steps; i++) {
                    double s = (double) i / Math.max(1, (int) (len * 3.0D));
                    double amp = 0.55D * Math.sin(Math.PI * s) * (1.0D - 0.35D * progress);
                    double a = t.phase + s * 7.0D - t.age * 0.7D;
                    Vec3 pt = start.add(d.scale(len * s)).add(u.scale(Math.sin(a) * amp)).add(w.scale(Math.cos(a) * amp));
                    level.sendParticles(i % 3 == 0 ? CYAN : BLUE, pt.x, pt.y, pt.z, 1, 0.0D, 0.0D, 0.0D, 0.0D);
                }
            }
            if (t.age == 6 && t.primary) {
                t.target.hurt(t.owner.damageSources().playerAttack(t.owner), 8.0F);
                t.target.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1), t.owner);
                level.sendParticles(ParticleTypes.ELECTRIC_SPARK, end.x, end.y, end.z, 14, 0.4D, 0.4D, 0.4D, 0.15D);
                level.sendParticles(ParticleTypes.GLOW, end.x, end.y, end.z, 6, 0.4D, 0.4D, 0.4D, 0.05D);
            }
            t.age++;
        }
    }

    private DreamAbilities() {
    }
}
