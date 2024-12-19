<template>
  <header class='app-header'>
    <div class="container">
      <h1 class="logo">
        <RouterLink to="/"></RouterLink>
      </h1>
      <ul class="app-header-nav">
        <li class="home">
          <RouterLink to="/">图谱仓库</RouterLink>
        </li>
      </ul>
      <div class="search">
        <i class="iconfont icon-search"></i>
        <input 
          type="text" 
          placeholder="搜一搜" 
          v-model="searchQuery" 
          @keyup.enter="handleSearch"
        >
        <button @click="handleSearch">搜索</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import emitter from './eventBus.js'

const searchQuery = ref('')

const handleSearch = async () => {
  if (searchQuery.value.trim()) {
    try {
      const response = await axios.get('http://127.0.0.1:8000/chapters/search_chapters/', {
        params: { q: searchQuery.value }
      })
      // 打印完整的 response
      console.log('Response:', response)
      // 打印 response 中的数据
      console.log('Response Data:', response.data)
      emitter.emit('search', response.data);
    } catch (error) {
      console.error('搜索失败:', error)
    }
  }
}

</script>

<style scoped lang='scss'>
.app-header {
  background: #fff;

  .container {
    display: flex;
    align-items: center;
  }

  .logo {
    width: 150px;

    a {
      display: block;
      height: 125px;
      width: 100%;
      text-indent: -9999px;
      background: url('@/assets/images/logo.png') no-repeat center 18px / contain;
    }
  }

  .app-header-nav {
    width: 820px;
    display: flex;
    padding-left: 40px;
    position: relative;
    z-index: 998;

    li {
      margin-right: 40px;
      width: 38px;
      text-align: center;

      a {
        margin-top: 10px;
        font-weight: bolder;
        font-size: 16px;
        line-height: 32px;
        height: 32px;
        width: 70px;
        display: inline-block;

        &:hover {
          color: $xtxColor;
          border-bottom: 1px solid $xtxColor;
        }
      }

      .active {
        color: $xtxColor;
        border-bottom: 1px solid $xtxColor;
      }
    }
  }

  .search {
    width: 170px;
    height: 32px;
    position: relative;
    border-bottom: 1px solid #e7e7e7;
    line-height: 32px;

    .icon-search {
      font-size: 18px;
      margin-left: 5px;
    }

    input {
      width: 140px;
      padding-left: 5px;
      color: #666;
    }
  }
}
</style>