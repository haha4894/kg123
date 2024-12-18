<template>
    <div class="node-info-overlay">
      <button @click="$emit('close')" class="close-btn">X</button>
      <h3>{{nodeData.name}}</h3>
      <p>{{nodeData.info}}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      nodeData: Object
    }
  }
  </script>
  
  <style scoped>
  .node-info-overlay {
    position: absolute;
    top: 0;
    right: 0;
    width: 300px;
    height: 100%;
    background: rgba(255,255,255,0.8);
    border-left: 1px solid #ccc;
    padding: 15px;
    box-sizing: border-box;
    z-index: 10;
    overflow-y: auto;
  }
  
  .close-btn {
    float: right;
    background: none;
    border: none;
    font-size: 16px;
    cursor: pointer;
  }
  </style>
  