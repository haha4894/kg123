<script setup>
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'

</script>

<script>
import emitter from './eventBus.js';

export default {
  methods: {
    onActionClick(action) {
      // 发送事件
      emitter.emit('custom-event', action);
    }
  }
}
</script>

<template>
  <el-row class="tac" >
    <el-col >
      <h5 class="mb-2">功能列表</h5>
      <el-menu
        default-active="2"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-sub-menu index="1">
          <template #title>
            <el-icon><location /></el-icon>
            <span>Navigator One</span>
          </template>
            <el-menu-item index="1-1" @click="onActionClick('action1')">根节点</el-menu-item>
            <el-menu-item index="1-2" @click="onActionClick('action2')">一级节点</el-menu-item>
            <el-menu-item index="1-3" @click="onActionClick('action3')">二级节点</el-menu-item>
            <el-menu-item index="1-4" @click="onActionClick('action4')">三级节点</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="2">
          <el-icon><icon-menu /></el-icon>
          <span>Navigator Two</span>
        </el-menu-item>
        <el-menu-item index="3" disabled>
          <el-icon><document /></el-icon>
          <span>Navigator Three</span>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><setting /></el-icon>
          <span>Navigator Four</span>
        </el-menu-item>
      </el-menu>
    </el-col>
  </el-row>
</template>

<style scoped lang="scss">
.tac{
  height: 670px;
  background-color: white;
  .mb-2{
    text-align: center;
    justify-content: center;
    font-size: 20px;
  }
}

</style>


