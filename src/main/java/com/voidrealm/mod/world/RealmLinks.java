package com.voidrealm.mod.world;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.registries.Registries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.ListTag;
import net.minecraft.nbt.Tag;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.datafix.DataFixTypes;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.saveddata.SavedData;

/** Nho cong nao nguoi choi da di vao de ve dung cho tu Void Realm. */
public class RealmLinks extends SavedData {
    private static final String NAME = "voidrealm_links";
    private final Map<UUID, GlobalPos> links = new HashMap<>();

    public static RealmLinks get(MinecraftServer server) {
        return server.overworld().getDataStorage()
                .computeIfAbsent(new SavedData.Factory<>(RealmLinks::new, RealmLinks::load, DataFixTypes.LEVEL), NAME);
    }

    public static RealmLinks load(CompoundTag tag, HolderLookup.Provider registries) {
        RealmLinks data = new RealmLinks();
        ListTag list = tag.getList("links", Tag.TAG_COMPOUND);
        for (int i = 0; i < list.size(); i++) {
            CompoundTag e = list.getCompound(i);
            ResourceKey<Level> dim = ResourceKey.create(Registries.DIMENSION, ResourceLocation.parse(e.getString("dim")));
            data.links.put(e.getUUID("id"), GlobalPos.of(dim, new BlockPos(e.getInt("x"), e.getInt("y"), e.getInt("z"))));
        }
        return data;
    }

    @Override
    public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
        ListTag list = new ListTag();
        for (Map.Entry<UUID, GlobalPos> entry : this.links.entrySet()) {
            CompoundTag e = new CompoundTag();
            e.putUUID("id", entry.getKey());
            e.putString("dim", entry.getValue().dimension().location().toString());
            e.putInt("x", entry.getValue().pos().getX());
            e.putInt("y", entry.getValue().pos().getY());
            e.putInt("z", entry.getValue().pos().getZ());
            list.add(e);
        }
        tag.put("links", list);
        return tag;
    }

    public GlobalPos get(UUID player) {
        return this.links.get(player);
    }

    public void put(UUID player, GlobalPos pos) {
        this.links.put(player, pos);
        this.setDirty();
    }
}
