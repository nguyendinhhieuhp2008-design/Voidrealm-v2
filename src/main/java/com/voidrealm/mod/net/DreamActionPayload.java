package com.voidrealm.mod.net;

import com.voidrealm.mod.VoidRealm;
import net.minecraft.network.RegistryFriendlyByteBuf;
import net.minecraft.network.codec.ByteBufCodecs;
import net.minecraft.network.codec.StreamCodec;
import net.minecraft.network.protocol.common.custom.CustomPacketPayload;
import net.minecraft.resources.ResourceLocation;

/** Client -> server: 0 = tang toc, 1 = xuc tu. */
public record DreamActionPayload(int action) implements CustomPacketPayload {
    public static final Type<DreamActionPayload> TYPE =
            new Type<>(ResourceLocation.fromNamespaceAndPath(VoidRealm.MODID, "dream_action"));
    public static final StreamCodec<RegistryFriendlyByteBuf, DreamActionPayload> CODEC =
            StreamCodec.composite(ByteBufCodecs.VAR_INT, DreamActionPayload::action, DreamActionPayload::new);

    @Override
    public Type<? extends CustomPacketPayload> type() {
        return TYPE;
    }
}
