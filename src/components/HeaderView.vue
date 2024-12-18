<template>
  <img class="logo" src="../assets/logo.png" alt="Logo"/>
    <header class="header">
      <div class="search-container">
        <div class="search-wrapper">
          <input 
            type="text" 
            class="search-input"
            placeholder="搜索关键字..." 
            v-model="searchValue" 
            @keyup.enter="onSearchEnter"
          />
          <button class="search-button" @click="onSearchEnter"></button>
        </div>
      </div>
    </header>
  </template>
  
  <script>
  import { ref } from 'vue'
  
  export default {
    emits:['onSearch'],
    setup(props, {emit}) {
      const searchValue = ref('')
  
      const onSearchEnter = () => {
        emit('onSearch', searchValue.value)
      }
  
      return {
        searchValue,
        onSearchEnter
      }
    }
  }
  </script>
  
  <style scoped>
    .header {
    flex: 0 0 80px;
    display: flex;
    align-items: center;    /* 垂直居中 */
    justify-content: flex-start; /* logo在左侧 */
    background: #fff;
    border-bottom: 1px solid #ccc;
    box-sizing: border-box;
    padding: 0 2px;
  } 
  .logo {
  position: absolute;
  top: 10px; /* 根据需要调整 */
  left: 10px; /* 根据需要调整 */
  max-width: 100px; /* 根据需要调整 */
  max-height: 100px; /* 根据需要调整 */
}
  
  /* 中间用search-container来水平居中搜索框 */
  .search-container {
    flex: 1; 
    display: flex;
    justify-content: center; /* 水平居中搜索区域 */
    align-items: center;     /* 垂直居中 */
  }
  
  /* search-wrapper是固定宽度容器 */
  .search-wrapper {
    position: relative;
    width: 450px;
  }
  
  .search-input {
    width: 100%;
    height: 30px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
    padding: 0 50px 0 10px; /* 右侧留出空间给按钮 */
    font-size: 18px;
  }
  
  /* 搜索按钮：绝对定位在输入框右侧 */
  .search-button {
    position: absolute;
    top: 50%;
    right: 0;
    transform: translateY(-50%);
    width: 50px;
    height: 50px;
    border: none;
    background: url('/src/assets/magnifying_glass.png') no-repeat center center;
    background-size: 20px 20px;
    cursor: pointer;
  } 
  </style>
  