<script setup>
import LayoutHeader from './components/LayoutHeader.vue';
import LayoutMeum from './components/LayoutMeum.vue';
import LayoutGraph from './components/LayoutGraph.vue';

</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header height="150px" class="header">
        <LayoutHeader></LayoutHeader>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <LayoutMeum/>
        </el-aside>
        <el-main><LayoutGraph/></el-main>
        <!-- <el-main>Main</el-main> -->
      </el-container>
    </el-container>
  </div>

</template>

<style scoped lang='scss'>
  .header{
    padding: 0px;
  }
</style>
