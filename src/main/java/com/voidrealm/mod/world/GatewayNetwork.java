package com.voidrealm.mod.world;

import java.util.ArrayList;
import java.util.List;
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

/** Danh sach moi Cong Dich Chuyen trong the gioi (luu cung save, khong phu thuoc chunk dang tai). */
public class GatewayNetwork extends SavedData {
    private static final String NAME = "voidrealm_gateways";
    private final List<GlobalPos> gateways = new ArrayList<>();

    public static GatewayNetwork get(MinecraftServer server) {
        return server.overworld().getDataStorage()
                .computeIfAbsent(new SavedData.Factory<>(GatewayNetwork::new, GatewayNetwork::load, DataFixTypes.LEVEL), NAME);
    }

    public static GatewayNetwork load(CompoundTag tag, HolderLookup.Provider registries) {
        GatewayNetwork network = new GatewayNetwork();
        ListTag list = tag.getList("gateways", Tag.TAG_COMPOUND);
        for (int i = 0; i < list.size(); i++) {
            CompoundTag entry = list.getCompound(i);
            ResourceLocation dim = ResourceLocation.parse(entry.getString("dim"));
            ResourceKey<Level> key = ResourceKey.create(Registries.DIMENSION, dim);
            network.gateways.add(GlobalPos.of(key, new BlockPos(entry.getInt("x"), entry.getInt("y"), entry.getInt("z"))));
        }
        return network;
    }

    @Override
    public CompoundTag save(CompoundTag tag, HolderLookup.Provider registries) {
        ListTag list = new ListTag();
        for (GlobalPos pos : this.gateways) {
            CompoundTag entry = new CompoundTag();
            entry.putString("dim", pos.dimension().location().toString());
            entry.putInt("x", pos.pos().getX());
            entry.putInt("y", pos.pos().getY());
            entry.putInt("z", pos.pos().getZ());
            list.add(entry);
        }
        tag.put("gateways", list);
        return tag;
    }

    public void add(GlobalPos pos) {
        if (!this.gateways.contains(pos)) {
            this.gateways.add(pos);
            this.setDirty();
        }
    }

    public void remove(GlobalPos pos) {
        if (this.gateways.remove(pos)) {
            this.setDirty();
        }
    }

    public List<GlobalPos> all() {
        return new ArrayList<>(this.gateways);
    }
}
