package com.voidrealm.mod.registry;

import com.voidrealm.mod.VoidRealm;
import com.voidrealm.mod.block.RiftLanternBlock;
import com.voidrealm.mod.block.VoidAltarBlock;
import com.voidrealm.mod.block.VoidFluxBlock;
import com.voidrealm.mod.block.VoidGatewayBlock;
import com.voidrealm.mod.block.VoidOreBlock;
import com.voidrealm.mod.block.VoidPortalBlock;
import com.voidrealm.mod.block.VoidPortalFrameBlock;
import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.SlabBlock;
import net.minecraft.world.level.block.StairBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.minecraft.world.level.material.PushReaction;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(VoidRealm.MODID);

    public static final DeferredHolder<Block, Block> VOID_CRYSTAL_ORE = BLOCKS.register("void_crystal_ore",
            () -> new VoidOreBlock(UniformInt.of(3, 7),
                    BlockBehaviour.Properties.of()
                            .mapColor(MapColor.STONE)
                            .strength(3.5F, 3.0F)
                            .requiresCorrectToolForDrops()
                            .sound(SoundType.STONE)));

    public static final DeferredHolder<Block, Block> DEEPSLATE_VOID_CRYSTAL_ORE = BLOCKS.register("deepslate_void_crystal_ore",
            () -> new VoidOreBlock(UniformInt.of(3, 7),
                    BlockBehaviour.Properties.of()
                            .mapColor(MapColor.DEEPSLATE)
                            .strength(4.5F, 3.0F)
                            .requiresCorrectToolForDrops()
                            .sound(SoundType.DEEPSLATE)));

    public static final DeferredHolder<Block, Block> VOID_STEEL_BLOCK = BLOCKS.register("void_steel_block",
            () -> new Block(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(5.0F, 6.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.METAL)));

    public static final DeferredHolder<Block, Block> VOID_STONE = BLOCKS.register("void_stone",
            () -> new Block(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_BLACK)
                    .strength(2.0F, 6.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.STONE)));

    public static final DeferredHolder<Block, Block> VOID_BRICKS = BLOCKS.register("void_bricks",
            () -> new Block(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_BLACK)
                    .strength(2.0F, 6.0F)
                    .requiresCorrectToolForDrops()
                    .sound(SoundType.STONE)));

    public static final DeferredHolder<Block, Block> RIFT_LANTERN = BLOCKS.register("rift_lantern",
            () -> new RiftLanternBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(1.5F)
                    .lightLevel(state -> 13)
                    .noOcclusion()
                    .emissiveRendering((state, level, pos) -> true)
                    .sound(SoundType.GLASS)));

    public static final DeferredHolder<Block, Block> VOID_GATEWAY = BLOCKS.register("void_gateway",
            () -> new VoidGatewayBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(4.0F, 1200.0F)
                    .requiresCorrectToolForDrops()
                    .lightLevel(state -> 11)
                    .noOcclusion()
                    .sound(SoundType.AMETHYST)));

    public static final DeferredHolder<Block, Block> VOID_FLUX = BLOCKS.register("void_flux",
            () -> new VoidFluxBlock(BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .noCollission()
                    .noOcclusion()
                    .replaceable()
                    .instabreak()
                    .lightLevel(state -> 11)
                    .pushReaction(PushReaction.DESTROY)
                    .isViewBlocking((state, level, pos) -> false)
                    .isSuffocating((state, level, pos) -> false)
                    .sound(SoundType.EMPTY)));

    // ---------------------------------------------------------------- Khoi xay dung & Void Realm
    private static BlockBehaviour.Properties stoneProps(float hardness) {
        return BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(hardness, 9.0F)
                .requiresCorrectToolForDrops().sound(SoundType.DEEPSLATE_BRICKS);
    }

    public static final DeferredHolder<Block, Block> VOID_TILE = BLOCKS.register("void_tile",
            () -> new Block(stoneProps(2.5F)));

    public static final DeferredHolder<Block, Block> VOID_PILLAR = BLOCKS.register("void_pillar",
            () -> new RotatedPillarBlock(stoneProps(2.5F)));

    public static final DeferredHolder<Block, Block> VOID_CHISELED = BLOCKS.register("void_chiseled",
            () -> new Block(stoneProps(2.5F).lightLevel(state -> 9)));

    public static final DeferredHolder<Block, Block> VOID_SOIL = BLOCKS.register("void_soil",
            () -> new Block(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(0.8F)
                    .sound(SoundType.ROOTED_DIRT)));

    public static final DeferredHolder<Block, Block> VOID_CRYSTAL_BLOCK = BLOCKS.register("void_crystal_block",
            () -> new Block(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(1.5F)
                    .requiresCorrectToolForDrops().lightLevel(state -> 12).sound(SoundType.AMETHYST)));

    public static final DeferredHolder<Block, Block> VOID_BRICKS_STAIRS = BLOCKS.register("void_bricks_stairs",
            () -> new StairBlock(VOID_BRICKS.get().defaultBlockState(), stoneProps(2.5F)));

    public static final DeferredHolder<Block, Block> VOID_BRICKS_SLAB = BLOCKS.register("void_bricks_slab",
            () -> new SlabBlock(stoneProps(2.5F)));

    public static final DeferredHolder<Block, Block> VOID_PORTAL_FRAME = BLOCKS.register("void_portal_frame",
            () -> new VoidPortalFrameBlock(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(30.0F, 1200.0F)
                    .requiresCorrectToolForDrops().lightLevel(state -> state.getValue(VoidPortalFrameBlock.LIT) ? 12 : 2)
                    .sound(SoundType.DEEPSLATE_BRICKS)));

    public static final DeferredHolder<Block, Block> VOID_PORTAL = BLOCKS.register("void_portal",
            () -> new VoidPortalBlock(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(-1.0F, 3600000.0F)
                    .noCollission().noOcclusion().lightLevel(state -> 13).pushReaction(PushReaction.BLOCK)
                    .sound(SoundType.EMPTY)));

    public static final DeferredHolder<Block, Block> VOID_ALTAR = BLOCKS.register("void_altar",
            () -> new VoidAltarBlock(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(30.0F, 1200.0F)
                    .requiresCorrectToolForDrops().noOcclusion()
                    .lightLevel(state -> state.getValue(VoidAltarBlock.STAGE) > 0 ? 14 : 6)
                    .sound(SoundType.DEEPSLATE_BRICKS)));

    private ModBlocks() {
    }
}
