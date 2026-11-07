package com.voidrealm.mod.block;

import com.voidrealm.mod.Config;
import com.voidrealm.mod.effect.Fx;
import com.voidrealm.mod.registry.ModBlocks;
import com.voidrealm.mod.world.RealmConstants;
import java.util.List;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.ItemInteractionResult;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LightningBolt;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.context.BlockPlaceContext;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Mirror;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.DirectionProperty;
import net.minecraft.world.level.block.state.properties.IntegerProperty;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.Vec3;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/**
 * Ban Te Hu Khong: dat o tam den tho. Nem Trung Rong Ender vao khu den tho (hoac chuot phai bang trung)
 * de bat dau nghi le: khung cong phat sang va mat cong 5x5 dan hien ra tung hang.
 * FACING chi huong tu ban te ve phia cong.
 */
public class VoidAltarBlock extends Block {
    public static final DirectionProperty FACING = BlockStateProperties.HORIZONTAL_FACING;
    public static final IntegerProperty STAGE = IntegerProperty.create("stage", 0, 7);
    private static final VoxelShape SHAPE = Shapes.or(
            Block.box(0.0D, 0.0D, 0.0D, 16.0D, 4.0D, 16.0D),
            Block.box(0.0D, 4.0D, 0.0D, 16.0D, 12.0D, 2.0D),
            Block.box(0.0D, 4.0D, 14.0D, 16.0D, 12.0D, 16.0D),
            Block.box(0.0D, 4.0D, 2.0D, 2.0D, 12.0D, 14.0D),
            Block.box(14.0D, 4.0D, 2.0D, 16.0D, 12.0D, 14.0D));

    public VoidAltarBlock(Properties properties) {
        super(properties);
        this.registerDefaultState(this.stateDefinition.any().setValue(FACING, Direction.SOUTH).setValue(STAGE, 0));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING, STAGE);
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        return this.defaultBlockState().setValue(FACING, context.getHorizontalDirection());
    }

    @Override
    protected BlockState rotate(BlockState state, Rotation rotation) {
        return state.setValue(FACING, rotation.rotate(state.getValue(FACING)));
    }

    @Override
    protected BlockState mirror(BlockState state, Mirror mirror) {
        return state.rotate(mirror.getRotation(state.getValue(FACING)));
    }

    @Override
    protected VoxelShape getShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext context) {
        return SHAPE;
    }

    @Override
    protected void onPlace(BlockState state, Level level, BlockPos pos, BlockState oldState, boolean movedByPiston) {
        if (!level.isClientSide && state.getValue(STAGE) < 7) {
            level.scheduleTick(pos, this, 10);
        }
    }

    @Override
    protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
        if (!level.isClientSide) {
            String key = state.getValue(STAGE) == 0 ? "message.voidrealm.altar_hint" : "message.voidrealm.altar_busy";
            player.displayClientMessage(Component.translatable(key), true);
        }
        return InteractionResult.sidedSuccess(level.isClientSide);
    }

    @Override
    protected ItemInteractionResult useItemOn(ItemStack stack, BlockState state, Level level, BlockPos pos, Player player,
                                              InteractionHand hand, BlockHitResult hit) {
        if (stack.is(Items.DRAGON_EGG) && state.getValue(STAGE) == 0) {
            if (level instanceof ServerLevel server) {
                if (!player.isCreative()) {
                    stack.shrink(1);
                }
                startRitual(server, pos, state);
            }
            return ItemInteractionResult.sidedSuccess(level.isClientSide);
        }
        return ItemInteractionResult.PASS_TO_DEFAULT_BLOCK_INTERACTION;
    }

    // ------------------------------------------------------------------ nghi le
    private void startRitual(ServerLevel level, BlockPos pos, BlockState state) {
        level.setBlock(pos, state.setValue(STAGE, 1), Block.UPDATE_ALL);
        strike(level, Vec3.atBottomCenterOf(pos));
        level.playSound(null, pos, SoundEvents.ENDER_DRAGON_GROWL, SoundSource.BLOCKS, 1.2F, 0.7F);
        level.scheduleTick(pos, this, 40);
    }

    private static void strike(ServerLevel level, Vec3 at) {
        LightningBolt bolt = EntityType.LIGHTNING_BOLT.create(level);
        if (bolt != null) {
            bolt.moveTo(at);
            bolt.setVisualOnly(true);
            level.addFreshEntity(bolt);
        }
    }

    @Override
    protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
        int stage = state.getValue(STAGE);
        Direction facing = state.getValue(FACING);
        if (stage == 0) {
            List<ItemEntity> eggs = level.getEntitiesOfClass(ItemEntity.class, new AABB(pos).inflate(9.0D, 5.0D, 9.0D),
                    e -> e.isAlive() && e.getItem().is(Items.DRAGON_EGG));
            if (!eggs.isEmpty()) {
                ItemEntity egg = eggs.get(0);
                Fx.burst(level, egg.getX(), egg.getY() + 0.3D, egg.getZ(), ParticleTypes.PORTAL, 40, 0.3D, 0.6D);
                egg.getItem().shrink(1);
                if (egg.getItem().isEmpty()) {
                    egg.discard();
                }
                startRitual(level, pos, state);
            } else {
                level.scheduleTick(pos, this, 10);
            }
            return;
        }
        if (stage == 1) {
            lightFrame(level, pos, facing);
            beams(level, pos, facing, 1.0F);
            level.setBlock(pos, state.setValue(STAGE, 2), Block.UPDATE_ALL);
            level.scheduleTick(pos, this, 30);
            return;
        }
        if (stage <= 6) {
            int row = stage - 2;
            fillRow(level, pos, facing, row);
            beams(level, pos, facing, 0.6F);
            level.playSound(null, gatePos(pos, facing, 0, row), SoundEvents.AMETHYST_BLOCK_RESONATE, SoundSource.BLOCKS, 1.4F, 0.6F + row * 0.15F);
            level.setBlock(pos, state.setValue(STAGE, stage + 1), Block.UPDATE_ALL);
            if (stage < 6) {
                level.scheduleTick(pos, this, 30);
            } else {
                BlockPos center = gatePos(pos, facing, 0, 2);
                level.playSound(null, center, SoundEvents.END_PORTAL_SPAWN, SoundSource.BLOCKS, 1.5F, 1.0F);
                Fx.burst(level, center.getX() + 0.5D, center.getY() + 0.5D, center.getZ() + 0.5D, ParticleTypes.END_ROD, 120, 2.0D, 0.4D);
                strike(level, Vec3.atBottomCenterOf(center));
            }
        }
    }

    /** Vi tri o thuoc canh cong: right = lech ngang, up = do cao so voi hang day cua mat cong (hang 0). */
    public static BlockPos gatePos(BlockPos altar, Direction facing, int right, int up) {
        return altar.relative(facing, RealmConstants.GATE_FWD).relative(facing.getCounterClockWise(), right).above(up);
    }

    private static void lightFrame(ServerLevel level, BlockPos altar, Direction facing) {
        for (int right = -3; right <= 3; right++) {
            for (int up = -1; up <= 5; up++) {
                boolean ring = Math.abs(right) == 3 || up == -1 || up == 5;
                if (!ring) {
                    continue;
                }
                BlockPos p = gatePos(altar, facing, right, up);
                BlockState s = level.getBlockState(p);
                if (s.is(ModBlocks.VOID_PORTAL_FRAME.get())) {
                    level.setBlock(p, s.setValue(VoidPortalFrameBlock.LIT, true), Block.UPDATE_ALL);
                }
            }
        }
    }

    private static void fillRow(ServerLevel level, BlockPos altar, Direction facing, int row) {
        Direction.Axis axis = facing.getAxis() == Direction.Axis.Z ? Direction.Axis.X : Direction.Axis.Z;
        BlockState portal = ModBlocks.VOID_PORTAL.get().defaultBlockState().setValue(VoidPortalBlock.AXIS, axis);
        for (int right = -2; right <= 2; right++) {
            BlockPos p = gatePos(altar, facing, right, row);
            if (level.getBlockState(p).isAir()) {
                level.setBlock(p, portal, Block.UPDATE_ALL);
                Fx.burst(level, p.getX() + 0.5D, p.getY() + 0.5D, p.getZ() + 0.5D, ParticleTypes.END_ROD, 6, 0.3D, 0.1D);
            }
        }
    }

    /** Tia nang luong tu dinh 8 cot dan ve tam cong. */
    private static void beams(ServerLevel level, BlockPos altar, Direction facing, float strength) {
        Vec3 target = Vec3.atCenterOf(gatePos(altar, facing, 0, 2));
        Direction right = facing.getCounterClockWise();
        for (int i = 0; i < 8; i++) {
            double angle = Math.toRadians(22.5D + 45.0D * i);
            double lx = Math.sin(angle) * RealmConstants.PILLAR_R;
            double lz = Math.cos(angle) * RealmConstants.PILLAR_R;
            double wx = altar.getX() + 0.5D + facing.getStepX() * lz + right.getStepX() * lx;
            double wz = altar.getZ() + 0.5D + facing.getStepZ() * lz + right.getStepZ() * lx;
            Vec3 top = new Vec3(wx, altar.getY() + RealmConstants.PILLAR_TOP_DY, wz);
            Fx.line(level, top, target, i % 2 == 0 ? ParticleTypes.END_ROD : ParticleTypes.REVERSE_PORTAL, 1.6D / strength);
            Fx.burst(level, top.x, top.y, top.z, ParticleTypes.PORTAL, 14, 0.6D, 0.3D);
        }
    }

    @Override
    public void animateTick(BlockState state, Level level, BlockPos pos, RandomSource random) {
        int stage = state.getValue(STAGE);
        if (Config.roll(random, stage == 0 ? 6 : 1)) {
            level.addParticle(stage == 0 ? ParticleTypes.REVERSE_PORTAL : ParticleTypes.END_ROD,
                    pos.getX() + 0.2D + random.nextDouble() * 0.6D, pos.getY() + 0.8D, pos.getZ() + 0.2D + random.nextDouble() * 0.6D,
                    0.0D, 0.05D + stage * 0.01D, 0.0D);
        }
    }
}
