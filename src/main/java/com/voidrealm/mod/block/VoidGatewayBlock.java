package com.voidrealm.mod.block;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.effect.Fx;
import com.voidrealm.mod.registry.ModItems;
import com.voidrealm.mod.world.GatewayNetwork;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.GlobalPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * Cong Dich Chuyen Hu Khong: chuot phai de nhay den cong tiep theo (Shift + chuot phai: cong truoc do).
 * Ton Manh Hu Khong (nhien lieu) trong tui do: xa hon thi ton nhieu hon.
 */
public class VoidGatewayBlock extends Block {
    private static final VoxelShape SHAPE = Block.box(0.0D, 0.0D, 0.0D, 16.0D, 5.0D, 16.0D);

    public VoidGatewayBlock(Properties properties) {
        super(properties);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }

    @Override
    protected void onPlace(BlockState state, Level level, BlockPos pos, BlockState oldState, boolean movedByPiston) {
        if (!level.isClientSide && !oldState.is(this) && level.getServer() != null) {
            GatewayNetwork.get(level.getServer()).add(GlobalPos.of(level.dimension(), pos));
        }
        super.onPlace(state, level, pos, oldState, movedByPiston);
    }

    @Override
    protected void onRemove(BlockState state, Level level, BlockPos pos, BlockState newState, boolean movedByPiston) {
        if (!level.isClientSide && !state.is(newState.getBlock()) && level.getServer() != null) {
            GatewayNetwork.get(level.getServer()).remove(GlobalPos.of(level.dimension(), pos));
        }
        super.onRemove(state, level, pos, newState, movedByPiston);
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (level.isClientSide) {
            return InteractionResult.SUCCESS;
        }
        MinecraftServer server = level.getServer();
        if (server == null || !(player instanceof ServerPlayer sp)) {
            return InteractionResult.PASS;
        }
        GatewayNetwork network = GatewayNetwork.get(server);
        GlobalPos here = GlobalPos.of(level.dimension(), pos);
        network.add(here);
        List<GlobalPos> list = network.all();
        if (list.size() < 2) {
            sp.displayClientMessage(Component.translatable("message.voidrealm.gateway_alone"), true);
            return InteractionResult.SUCCESS;
        }
        int index = list.indexOf(here);
        int step = player.isShiftKeyDown() ? -1 : 1;
        GlobalPos target = list.get(Math.floorMod(index + step, list.size()));
        ServerLevel destLevel = server.getLevel(target.dimension());
        if (destLevel == null) {
            network.remove(target);
            return InteractionResult.SUCCESS;
        }
        BlockPos dest = target.pos();
        destLevel.getChunkAt(dest);
        if (!destLevel.getBlockState(dest).is(this)) {
            network.remove(target);
            sp.displayClientMessage(Component.translatable("message.voidrealm.gateway_missing"), true);
            return InteractionResult.SUCCESS;
        }

        int cost = 1;
        if (target.dimension() != level.dimension()) {
            cost = 3;
        } else {
            double dist = Math.sqrt(pos.distSqr(dest));
            cost = (int) Math.min(5, 1 + dist / 400.0D);
        }
        if (!sp.isCreative() && countFuel(sp) < cost) {
            sp.displayClientMessage(Component.translatable("message.voidrealm.gateway_fuel", cost), true);
            level.playSound(null, pos, SoundEvents.BEACON_DEACTIVATE, SoundSource.BLOCKS, 0.6F, 1.5F);
            return InteractionResult.SUCCESS;
        }
        if (!sp.isCreative()) {
            takeFuel(sp, cost);
        }

        ServerLevel origin = (ServerLevel) level;
        Fx.burst(origin, pos.getX() + 0.5D, pos.getY() + 1.2D, pos.getZ() + 0.5D, ParticleTypes.REVERSE_PORTAL, 40, 0.5D, 0.3D);
        Fx.ring(origin, pos.getX() + 0.5D, pos.getY() + 0.3D, pos.getZ() + 0.5D, 1.5D, ParticleTypes.END_ROD, 24, -0.3D);
        origin.playSound(null, pos, SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 1.0F, 0.7F);

        sp.teleportTo(destLevel, dest.getX() + 0.5D, dest.getY() + 0.35D, dest.getZ() + 0.5D, sp.getYRot(), sp.getXRot());
        sp.resetFallDistance();

        Fx.burst(destLevel, dest.getX() + 0.5D, dest.getY() + 1.2D, dest.getZ() + 0.5D, ParticleTypes.REVERSE_PORTAL, 40, 0.5D, 0.3D);
        Fx.ring(destLevel, dest.getX() + 0.5D, dest.getY() + 0.3D, dest.getZ() + 0.5D, 1.5D, ParticleTypes.END_ROD, 24, 0.3D);
        destLevel.playSound(null, dest, SoundEvents.ENDERMAN_TELEPORT, SoundSource.PLAYERS, 1.0F, 1.2F);
        sp.displayClientMessage(Component.translatable("message.voidrealm.gateway_jump",
                dest.getX(), dest.getY(), dest.getZ(), cost), true);
        return InteractionResult.SUCCESS;
    }

    private static int countFuel(ServerPlayer player) {
        int total = 0;
        for (ItemStack stack : player.getInventory().items) {
            if (stack.is(ModItems.VOID_SHARD.get())) {
                total += stack.getCount();
            }
        }
        return total;
    }

    private static void takeFuel(ServerPlayer player, int amount) {
        int left = amount;
        for (ItemStack stack : player.getInventory().items) {
            if (left <= 0) {
                break;
            }
            if (stack.is(ModItems.VOID_SHARD.get())) {
                int take = Math.min(left, stack.getCount());
                stack.shrink(take);
                left -= take;
            }
        }
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        double cx = pos.getX() + 0.5D;
        double cz = pos.getZ() + 0.5D;
        if (Config.roll(random, 2)) {
            double a = random.nextDouble() * Math.PI * 2.0D;
            level.addParticle(ParticleTypes.REVERSE_PORTAL, cx + Math.cos(a) * 0.9D, pos.getY() + 0.4D, cz + Math.sin(a) * 0.9D,
                    -Math.sin(a) * 0.05D, 0.07D, Math.cos(a) * 0.05D);
        }
        if (Config.roll(random, 5)) {
            level.addParticle(ParticleTypes.END_ROD, cx + (random.nextDouble() - 0.5D) * 0.5D, pos.getY() + 1.0D,
                    cz + (random.nextDouble() - 0.5D) * 0.5D, 0.0D, 0.03D, 0.0D);
        }
    }
}
