package com.voidrealm.mod.world;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.effect.Fx;
import com.voidrealm.mod.registry.ModBlocks;
import java.util.Optional;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructurePlaceSettings;
import net.minecraft.world.level.levelgen.structure.templatesystem.StructureTemplate;
import net.minecraft.world.phys.Vec3;

/** Di chuyen giua Overworld (hoac chieu khac) va chieu Void Realm qua cong Hu Khong. */
public final class RealmTravel {
    public static final ResourceKey<Level> REALM =
            ResourceKey.create(Registries.DIMENSION, ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "void_realm"));

    public static void travel(ServerPlayer player, ServerLevel from, BlockPos portalPos) {
        MinecraftServer server = from.getServer();
        if (from.dimension().equals(REALM)) {
            returnHome(player, from, server);
            return;
        }
        ServerLevel realm = server.getLevel(REALM);
        if (realm == null) {
            return;
        }
        ensureNexus(realm);
        RealmLinks.get(server).put(player.getUUID(), GlobalPos.of(from.dimension(), portalPos));
        Fx.burst(from, player.getX(), player.getY() + 1.0D, player.getZ(), ParticleTypes.REVERSE_PORTAL, 60, 0.6D, 0.4D);
        BlockPos arrive = RealmConstants.NEXUS_ORIGIN.offset(RealmConstants.ARRIVE_X, RealmConstants.ARRIVE_Y, RealmConstants.ARRIVE_Z);
        player.teleportTo(realm, arrive.getX() + 0.5D, arrive.getY(), arrive.getZ() + 0.5D, 180.0F, 0.0F);
        player.resetFallDistance();
        Fx.burst(realm, arrive.getX() + 0.5D, arrive.getY() + 1.0D, arrive.getZ() + 0.5D, ParticleTypes.END_ROD, 40, 0.6D, 0.2D);
        realm.playSound(null, arrive, SoundEvents.PORTAL_TRAVEL, SoundSource.PLAYERS, 0.5F, 0.8F);
    }

    private static void returnHome(ServerPlayer player, ServerLevel from, MinecraftServer server) {
        GlobalPos origin = RealmLinks.get(server).get(player.getUUID());
        ServerLevel dest = origin == null ? null : server.getLevel(origin.dimension());
        double x;
        double y;
        double z;
        if (origin != null && dest != null) {
            BlockPos spot = findSpotBeside(dest, origin.pos());
            x = spot.getX() + 0.5D;
            y = spot.getY();
            z = spot.getZ() + 0.5D;
        } else {
            dest = server.overworld();
            BlockPos spawn = dest.getSharedSpawnPos();
            x = spawn.getX() + 0.5D;
            z = spawn.getZ() + 0.5D;
            y = dest.getHeight(Heightmap.Types.MOTION_BLOCKING, spawn.getX(), spawn.getZ()) + 1.0D;
        }
        Fx.burst(from, player.getX(), player.getY() + 1.0D, player.getZ(), ParticleTypes.REVERSE_PORTAL, 60, 0.6D, 0.4D);
        player.teleportTo(dest, x, y, z, player.getYRot(), 0.0F);
        player.resetFallDistance();
        dest.playSound(null, BlockPos.containing(x, y, z), SoundEvents.PORTAL_TRAVEL, SoundSource.PLAYERS, 0.5F, 1.1F);
    }

    /** Tim cho dung canh mat cong (khong trung vao khoi dac). */
    private static BlockPos findSpotBeside(ServerLevel level, BlockPos portal) {
        level.getChunkAt(portal);
        for (int dist = 2; dist <= 4; dist++) {
            for (Direction dir : Direction.Plane.HORIZONTAL) {
                BlockPos feet = portal.relative(dir, dist);
                if (level.getBlockState(feet).isAir() && level.getBlockState(feet.above()).isAir()) {
                    return feet;
                }
            }
        }
        return portal.above(2);
    }

    /** Dung Trung Tam Hu Khong (cong ve) neu chua co. */
    public static void ensureNexus(ServerLevel realm) {
        BlockPos origin = RealmConstants.NEXUS_ORIGIN;
        BlockPos marker = origin.offset(RealmConstants.MARK_X, RealmConstants.MARK_Y, RealmConstants.MARK_Z);
        realm.getChunkAt(marker);
        if (realm.getBlockState(marker).is(ModBlocks.VOID_PORTAL.get())) {
            return;
        }
        Optional<StructureTemplate> template = realm.getStructureManager()
                .get(ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "void_nexus"));
        template.ifPresent(t -> t.placeInWorld(realm, origin, origin,
                new StructurePlaceSettings().setIgnoreEntities(true), realm.getRandom(), Block.UPDATE_CLIENTS));
    }

    private RealmTravel() {
    }
}
