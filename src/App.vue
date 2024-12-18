<template>
  <div class="app-container">
    <HeaderView @onSearch="handleSearch"/>
    <div class="main-content">
      <SidebarView :collapsed="sidebarCollapsed" @toggle="toggleSidebar"/>
      <div class="graph-container">
        <GraphView 
          @node-click="showNodeInfo" 
          @background-click="hideNodeInfo" 
          :searchKey="searchKey" 
        />
        <NodeInfoOverlay 
          v-if="selectedNode" 
          :nodeData="selectedNode" 
          @close="hideNodeInfo"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import HeaderView from './components/HeaderView.vue'
import SidebarView from './components/SidebarView.vue'
import GraphView from './components/GraphView.vue'
import NodeInfoOverlay from './components/NodeInfoOverlay.vue'

export default {
  components: { HeaderView, SidebarView, GraphView, NodeInfoOverlay },
  setup() {
    const sidebarCollapsed = ref(false)
    const searchKey = ref('')
    const selectedNode = ref(null)

    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
    }

    const handleSearch = (val) => {
      searchKey.value = val
    }

    const showNodeInfo = (nodeData) => {
      selectedNode.value = nodeData
    }

    const hideNodeInfo = () => {
      selectedNode.value = null
    }

    return {
      sidebarCollapsed,
      searchKey,
      selectedNode,
      toggleSidebar,
      handleSearch,
      showNodeInfo,
      hideNodeInfo
    }
  }
}
</script>

<style scoped>
/* 让整个界面占满视口高度 */
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}

/* 外层容器占满整个视口高度 */
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* 占据整个视口高度 */
  box-sizing: border-box;
  margin: 0;
}

/* main-content 除去 header (200px) 剩下的全部 */
.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* graph-container 占据除去sidebar以外的剩余空间 */
.graph-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #fff;
}
</style>
