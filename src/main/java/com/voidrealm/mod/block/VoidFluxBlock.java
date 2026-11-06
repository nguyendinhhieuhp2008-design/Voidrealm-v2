package com.voidrealm.mod.block;

import com.voidrealm.mod.Config;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.LevelAccessor;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.phys.Vec3;

/**
 * Thac Nuoc Nguoc (Void Flux): khoi nguon (age = 0) tu phun mot dong chay NGUOC LEN troi (toi da MAX_AGE khoi).
 * Moi sinh vat / vat roi trong dong se bi day bay len. Giu Shift de lo lung giua dong.
 */
public class VoidFluxBlock extends Block {
    public static final int MAX_AGE = 28;
    public static final IntegerProperty AGE = IntegerProperty.create("age", 0, MAX_AGE);

    public VoidFluxBlock(Properties properties) {
        super(properties);
        this.registerDefaultState(this.stateDefinition.any().setValue(AGE, 0));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(AGE);
    }

    @Override
    protected void onPlace(BlockState state, Level level, BlockPos pos, BlockState oldState, boolean movedByPiston) {
        level.scheduleTick(pos, this, 3);
    }

    @Override
    protected BlockState updateShape(BlockState state, Direction direction, BlockState neighborState,
                                     LevelAccessor level, BlockPos pos, BlockPos neighborPos) {
        if (direction == Direction.DOWN) {
            level.scheduleTick(pos, this, 2);
        }
        return state;
    }

    @Override
    protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        int age = state.getValue(AGE);
        if (age > 0) {
            BlockState below = level.getBlockState(pos.below());
            if (!(below.is(this) && below.getValue(AGE) == age - 1)) {
                level.removeBlock(pos, false);
                return;
            }
        }
        if (age < MAX_AGE) {
            BlockPos up = pos.above();
            if (level.getBlockState(up).isAir()) {
                level.setBlock(up, this.defaultBlockState().setValue(AGE, age + 1), Block.UPDATE_ALL);
            }
            level.scheduleTick(pos, this, 8);
        }
    }

    @Override
    protected void entityInside(BlockState state, Level level, BlockPos pos, Entity entity) {
        Vec3 motion = entity.getDeltaMovement();
        double y;
        if (entity.isShiftKeyDown()) {
            y = Math.max(motion.y * 0.8D, -0.15D);
        } else {
            y = Math.min(motion.y + 0.09D, 0.42D);
        }
        entity.setDeltaMovement(motion.x * 0.85D, y, motion.z * 0.85D);
        entity.resetFallDistance();
    }

    @Override
    protected boolean skipRendering(BlockState state, BlockState adjacentState, Direction direction) {
        return adjacentState.is(this);
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        if (Config.roll(random, 3)) {
            level.addParticle(ParticleTypes.REVERSE_PORTAL,
                    pos.getX() + random.nextDouble(), pos.getY() + random.nextDouble(), pos.getZ() + random.nextDouble(),
                    0.0D, 0.12D, 0.0D);
        }
        if (Config.roll(random, 9)) {
            level.addParticle(ParticleTypes.END_ROD,
                    pos.getX() + random.nextDouble(), pos.getY() + random.nextDouble(), pos.getZ() + random.nextDouble(),
                    0.0D, 0.1D, 0.0D);
        }
        if (state.getValue(AGE) == 0 && Config.roll(random, 4)) {
            level.addParticle(ParticleTypes.DRAGON_BREATH, pos.getX() + 0.5D, pos.getY() + 1.0D, pos.getZ() + 0.5D,
                    0.0D, 0.1D, 0.0D);
        }
    }
}
