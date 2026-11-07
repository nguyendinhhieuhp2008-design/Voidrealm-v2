package com.voidrealm.mod.block;

import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BooleanProperty;

/** Khung canh cong Hu Khong: cac ky tu phat sang khi nghi le kich hoat (lit = true). */
public class VoidPortalFrameBlock extends Block {
    public static final BooleanProperty LIT = BooleanProperty.create("lit");

    public VoidPortalFrameBlock(Properties properties) {
        super(properties);
        this.registerDefaultState(this.stateDefinition.any().setValue(LIT, false));
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(LIT);
    }
}
