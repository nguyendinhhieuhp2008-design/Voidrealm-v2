package com.voidrealm.mod.block;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.world.RealmTravel;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.EnumProperty;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.VoxelShape;

/** Mat cong Hu Khong (phang, xuyen qua duoc). Nguoi choi di vao se duoc dua toi / ve tu chieu Void Realm. */
public class VoidPortalBlock extends Block {
    public static final EnumProperty<Direction.Axis> AXIS = BlockStateProperties.HORIZONTAL_AXIS;
    private static final VoxelShape SHAPE_X = Block.box(0.0D, 0.0D, 6.0D, 16.0D, 16.0D, 10.0D);
    private static final VoxelShape SHAPE_Z = Block.box(6.0D, 0.0D, 0.0D, 10.0D, 16.0D, 16.0D);
    private static final String COOLDOWN_KEY = "voidrealm_portal_cd";

    public VoidPortalBlock(Properties properties) {
        super(properties);
        this.registerDefaultState(this.stateDefinition.any().setValue(AXIS, Direction.Axis.X));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(AXIS);
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return state.getValue(AXIS) == Direction.Axis.X ? SHAPE_X : SHAPE_Z;
    }

    @Override
    protected void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
        if (level.isClientSide || !(entity instanceof ServerPlayer player) || !(level instanceof ServerLevel serverLevel)) {
            return;
        }
        long now = level.getGameTime();
        if (player.getPersistentData().getLong(COOLDOWN_KEY) > now) {
            return;
        }
        player.getPersistentData().putLong(COOLDOWN_KEY, now + 80L);
        level.playSound(null, pos, SoundEvents.PORTAL_TRAVEL, SoundSource.BLOCKS, 0.4F, 1.4F);
        RealmTravel.travel(player, serverLevel, pos);
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        boolean xAxis = state.getValue(AXIS) == Direction.Axis.X;
        if (Config.roll(random, 2)) {
            double x = pos.getX() + random.nextDouble();
            double y = pos.getY() + random.nextDouble();
            double z = pos.getZ() + 0.5D + (random.nextDouble() - 0.5D) * 0.2D;
            if (!xAxis) {
                z = pos.getZ() + random.nextDouble();
                x = pos.getX() + 0.5D + (random.nextDouble() - 0.5D) * 0.2D;
            }
            level.addParticle(random.nextInt(3) == 0 ? ParticleTypes.END_ROD : ParticleTypes.REVERSE_PORTAL,
                    x, y, z, (random.nextDouble() - 0.5D) * 0.05D, 0.04D, (random.nextDouble() - 0.5D) * 0.05D);
        }
        if (random.nextInt(280) == 0) {
            level.playLocalSound(pos.getX() + 0.5D, pos.getY() + 0.5D, pos.getZ() + 0.5D,
                    SoundEvents.PORTAL_AMBIENT, SoundSource.BLOCKS, 0.5F, random.nextFloat() * 0.4F + 0.6F, false);
        }
    }
}
