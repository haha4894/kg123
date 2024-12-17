<template>
  <div :class="['sidebar', {collapsed}]">
    <div class="sidebar-header">
      <button @click="$emit('toggle')" class="toggle-btn">
        {{ collapsed ? '>' : '<' }}
      </button>
    </div>
    <!-- 按钮区域 -->
    <div class="sidebar-actions">
      <button class="action-btn" @click="onActionClick('action1')">Action 1</button>
      <button class="action-btn" @click="onActionClick('action2')">Action 2</button>
      <button class="action-btn" @click="onActionClick('action3')">Action 3</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    collapsed: Boolean
  },
  emits: ['action'],
  setup(props, {emit}) {
    const onActionClick = (action) => {
      emit('action', action)
    }
    return {
      onActionClick
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 100px;
  background: #fff;
  border-right: 1px solid #ccc;
  transition: width 0.3s;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar-header {
  padding:10px;
  box-sizing: border-box;
  border-bottom: 1px solid #ccc;
  display: flex;
  justify-content: flex-start;
}

.toggle-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
}

.sidebar-actions {
  display: flex;
  flex-direction: column;
  align-items: center;   /* 水平居中按钮 */
  padding-top: 20px;     /* 顶部留出一些空间 */
}

/* 普通按钮样式，间距100px */
.action-btn {
  width: 120px;
  height: 40px;
  background: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 100px;  /* 按钮之间垂直间距100px */
}

/* 可在悬停时改变背景颜色 */
.action-btn:hover {
  background: #ccc;
}

/* 去掉最后一个按钮与下方的多余间距，可根据需要处理 */
.sidebar-actions .action-btn:last-child {
  margin-bottom: 0;
}
</style>
