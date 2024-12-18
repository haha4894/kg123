<template>
  <div ref="d3Container" style="width: 100%; height: 600px;"></div>
  <button @click="showAllNodes">显示所有节点</button>
  <el-drawer
      :title="selectedNode ? selectedNode.name : '节点详情'"
      v-model="drawerVisible"
      :with-header="true"
    >
      <div v-if="selectedNode">
        <p>节点名称: {{ selectedNode.name }}</p>
        <p v-if="selectedNode.content">内容: {{ selectedNode.content }}</p>
        <p v-else>该节点没有内容。</p>
      </div>
      <div v-else>
        <p>请双击一个节点查看详情。</p>
      </div>
    </el-drawer>
</template>

<script>
import * as d3 from 'd3';
import emitter from './eventBus.js';
// import axios from 'axios';

// const response = await axios.get('http://127.0.0.1:8000/chapters/relations/');


const colors = ["#679fca", "#7fc97e", "#b15076","#6964ad","#d7a4b6"];
export default {
  name: 'D3ForceGraph',
  data() {
    return {
      width: 1450,
      height: 630,
      nodes: [],
      edges: [],
      tempEdges: [],
      nodesMap: {},
      linkMap: {},
      nodesData: [],
      forceSimulation: null,
      svg: null,
      g: null,
      links: null,
      linksText: null,
      gs: null,
      menuVisible: false,
      menuX: 0,
      menuY: 0,
      buttons: [
      { text: '收起', action: 'action1' },
      { text: '展开', action: 'action2' },
      { text: '查询', action: 'action3' }
    ],
      drawerVisible: false, // 控制 drawer 的显示与隐藏
      selectedNode: null, // 当前选中的节点
      // response: response.data
    };
  },
  mounted() {
    this.initData();
    this.initGraph();
    emitter.on('custom-event', this.handleAction);
  },
  methods: {
    initData() {
  this.nodes =
  [
    { id: 'root', name: '软件工程', visible: true, weight: 6 },
    { id: 'CH3', name: '第3章 敏捷和敏捷过程', weight: 5 },
    { id: 'CH6', name: '第6章 指导实践的原则', weight: 5 },
    { id: 'CH1', name: '第1章 软件与软件工程', weight: 5 },
    { id: 'T1.1', name: '1.1 软件的本质', weight: 4 },
    { id: 'T1.2', name: '1.2 定义软件工程学科', weight: 4 },
    { id: 'S1.1.1', name: '1.1.1 定义软件', weight: 3 },
    { id: 'S1.1.2', name: '1.1.2 软件应用领域', weight: 3 },
    { id: 'SS1.1.1.1', name: '1.1.1.1 软件的双重角色', weight: 2 },
    { id: 'SS1.1.1.2', name: '1.1.1.2 什么是软件', weight: 2 },
    { id: 'SS1.1.1.3', name: '1.1.1.3 软件与硬件具有不同的特性', weight: 2 },
    { id: 'P1.1.1.3.1', name: '1.1.1.3.1 软件是设计开发出的产品', weight: 1 },
    { id: 'P1.1.1.3.2', name: '1.1.1.3.2 软件不会“磨损”', weight: 1 },
    { id: 'P1.1.1.3.3', name: '1.1.1.3.3 基于构件的构造模式', weight: 1 },
    { id: 'S1.1.3', name: '1.1.3 遗留软件', weight: 3 },
    { id: 'P1.1.2.1.1', name: '1.1.2.1.1 系统软件', weight: 1 },
    { id: 'P1.1.2.1.2', name: '1.1.2.1.2 应用软件', weight: 1 },
    { id: 'P1.1.2.1.3', name: '1.1.2.1.3 工程/科学软件', weight: 1 },
    { id: 'P1.1.2.1.4', name: '1.1.2.1.4 嵌入式软件', weight: 1 },
    { id: 'P1.1.2.1.5', name: '1.1.2.1.5 产品线软件', weight: 1 },
    { id: 'P1.1.2.1.6', name: '1.1.2.1.6 Web/移动app', weight: 1 },
    { id: 'P1.1.2.1.7', name: '1.1.2.1.7 人工智能软件', weight: 1 },
    { id: 'SS1.1.3.1', name: '1.1.3.1 遗留软件的定义', weight: 2 },
    { id: 'SS1.1.3.2', name: '1.1.3.2 遗留软件的“质量差”问题', weight: 2 },
    { id: 'SS1.1.3.3', name: '1.1.3.3 遗留软件为什么要演化?', weight: 2 },
    { id: 'T1.3', name: '1.3 软件过程', weight: 4 },
    { id: 'S1.2.1', name: '1.2.1 软件工程的定义', weight: 3 },
    { id: 'S1.2.2', name: '1.2.2 软件工程是一种层次化技术', weight: 3 },
    { id: 'P1.2.2.1.1', name: '1.2.2.1.1 过程层', weight: 1 },
    { id: 'P1.2.2.1.2', name: '1.2.2.1.2 方法层', weight: 1 },
    { id: 'P1.2.2.1.3', name: '1.2.2.1.3 工具层', weight: 1 },
    { id: 'T1.4', name: '1.4 软件工程实践', weight: 4 },
    { id: 'S1.3.1', name: '1.3.1 过程框架', weight: 3 },
    { id: 'S1.3.2', name: '1.3.2 普适性活动', weight: 3 },
    { id: 'P1.3.1.1.1', name: '1.3.1.1.1 沟通', weight: 1 },
    { id: 'P1.3.1.1.2', name: '1.3.1.1.2 策划', weight: 1 },
    { id: 'P1.3.1.1.3', name: '1.3.1.1.3 建模', weight: 1 },
    { id: 'P1.3.1.1.4', name: '1.3.1.1.4 构建', weight: 1 },
    { id: 'P1.3.1.1.5', name: '1.3.1.1.5 部署', weight: 1 },
    { id: 'S1.3.3', name: '1.3.3 过程的适应性调整', weight: 3 },
    { id: 'P1.3.2.1.1', name: '1.3.2.1.1 软件项目跟踪和控制', weight: 1 },
    { id: 'P1.3.2.1.2', name: '1.3.2.1.2 风险管理', weight: 1 },
    { id: 'P1.3.2.1.3', name: '1.3.2.1.3 软件质量保证', weight: 1 },
    { id: 'P1.3.2.1.4', name: '1.3.2.1.4 技术评审', weight: 1 },
    { id: 'P1.3.2.1.5', name: '1.3.2.1.5 测量', weight: 1 },
    { id: 'P1.3.2.1.6', name: '1.3.2.1.6 软件配置管理', weight: 1 },
    { id: 'P1.3.2.1.7', name: '1.3.2.1.7 可复用性管理', weight: 1 },
    { id: 'P1.3.2.1.8', name: '1.3.2.1.8 工作产品的准备和生产', weight: 1 },
    { id: 'T1.5', name: '1.5 这一切都是如何开始的', weight: 4 },
    { id: 'S1.4.1', name: '1.4.1 软件工程实践的精髓', weight: 3 },
    { id: 'S1.4.2', name: '1.4.2 通用原则', weight: 3 },
    { id: 'SS1.4.1.1', name: '1.4.1.1 理解问题', weight: 2 },
    { id: 'SS1.4.1.2', name: '1.4.1.2 策划解决方案', weight: 2 },
    { id: 'SS1.4.1.3', name: '1.4.1.3 实施计划', weight: 2 },
    { id: 'SS1.4.1.4', name: '1.4.1.4 检查结果', weight: 2 },
    { id: 'P1.4.2.1.1', name: '1.4.2.1.1 第一原则：存在价值', weight: 1 },
    { id: 'P1.4.2.1.2', name: '1.4.2.1.2 第二原则：保持简洁', weight: 1 },
    { id: 'P1.4.2.1.3', name: '1.4.2.1.3 第三原则：保持愿景', weight: 1 },
    { id: 'P1.4.2.1.4', name: '1.4.2.1.4 第四原则：关注使用者', weight: 1 },
    { id: 'P1.4.2.1.5', name: '1.4.2.1.5 第五原则：面向未来', weight: 1 },
    { id: 'P1.4.2.1.6', name: '1.4.2.1.6 第六原则：提前计划复用', weight: 1 },
    { id: 'P1.4.2.1.7', name: '1.4.2.1.7 第七原则：认真思考', weight: 1 },
    { id: 'T1.6', name: '1.6 小结', weight: 4 },
    { id: 'CH6', name: '第6章 指导实践的原则', weight: 5 },
    { id: 'T3.1', name: '3.1 什么是敏捷', weight: 4 },
    { id: 'T3.2', name: '3.2 敏捷及变更成本', weight: 4 },
    { id: 'S3.1.1', name: '3.1.1 敏捷宣言', weight: 3 },
    { id: 'S3.1.2', name: '3.1.2 敏捷价值观', weight: 3 },
    { id: 'S3.1.3', name: '3.1.3 敏捷开发', weight: 3 },
    { id: 'S3.1.2.1', name: '3.1.2.1 沟通', weight: 2 },
    { id: 'S3.1.2.2', name: '3.1.2.2 简单', weight: 2 },
    { id: 'S3.1.2.3', name: '3.1.2.3 反馈', weight: 2 },
    { id: 'S3.1.2.4', name: '3.1.2.4 勇气', weight: 2 },
    { id: 'S3.1.2.5', name: '3.1.2.4 尊重（谦逊）', weight: 2 },
    { id: 'S3.1.4', name: '3.1.4 敏捷', weight: 3 },
    { id: 'SS3.1.4.1', name: '3.1.4.1 变化以及敏捷团队', weight: 2 },
    { id: 'SS3.1.4.2', name: '3.1.4.2 敏捷不仅仅是有效地响应变化', weight: 2 },
    { id: 'T3.3', name: '3.3 什么是敏捷过程', weight: 4 },
    { id: 'S3.2.1', name: '3.2.1 传统软件开发方法的变更', weight: 3 },
    { id: 'S3.2.2', name: '3.2.2 敏捷的变更', weight: 3 },
    { id: 'T3.4', name: '3.4 Scrum', weight: 4 },
    { id: 'S3.3.1', name: '3.3.1 敏捷原则', weight: 3 },
    { id: 'S3.3.2', name: '3.3.2 敏捷过程的特征', weight: 3 },
    { id: 'S3.3.3', name: '3.3.3 人的因素', weight: 3 },
    { id: 'SS3.3.2.1', name: '3.3.2.1 敏捷过程的三大假设', weight: 2 },
    { id: 'SS3.3.2.2', name: '3.3.2.2 敏捷过程的一个重要问题', weight: 2 },
    { id: 'SS3.3.3.1', name: '3.3.3.1 构造而非选择', weight: 2 },
    { id: 'SS3.3.3.2', name: '3.3.3.2 对敏捷团队以及成员的要求', weight: 2 },
    { id: 'P3.3.3.2.1', name: '3.3.3.2.1 基本能力', weight: 1 },
    { id: 'P3.3.3.2.2', name: '3.3.3.2.2 共同目标', weight: 1 },
    { id: 'P3.3.3.2.3', name: '3.3.3.2.3 精诚合作', weight: 1 },
    { id: 'P3.3.3.2.4', name: '3.3.3.2.4 决策能力', weight: 1 },
    { id: 'P3.3.3.2.5', name: '3.3.3.2.5 模糊问题解决能力', weight: 1 },
    { id: 'P3.3.3.2.6', name: '3.3.3.2.6 相互信任和尊重', weight: 1 },
    { id: 'P3.3.3.2.7', name: '3.3.3.2.7 自组织', weight: 1 },
    { id: 'T3.5', name: '3.5 其他敏捷过程', weight: 4 },
    { id: 'S3.4.1', name: '3.4.1 Scrum团队和制品', weight: 3 },
    { id: 'S3.4.2', name: '3.4.2 冲刺规划会议', weight: 3 },
    { id: 'S3.4.3', name: '3.4.3 每日Scrum会议', weight: 3 },
    { id: 'S3.4.4', name: '3.4.4 冲刺评审会议', weight: 3 },
    { id: 'S3.4.5', name: '3.4.5 冲刺回顾', weight: 3 },
    { id: 'T3.6', name: '3.6 小结', weight: 4 },
    { id: 'S3.5.1', name: '3.5.1 XP框架', weight: 3 },
    { id: 'S3.5.2', name: '3.5.2 看板法', weight: 3 },
    { id: 'SS3.5.1.1', name: '3.5.1.1 极限编程介绍', weight: 2 },
    { id: 'SS3.5.1.2', name: '3.5.1.2 极限编程活动', weight: 2 },
    { id: 'P3.5.1.2.1', name: '3.5.1.2.1 策划', weight: 1 },
    { id: 'P3.5.1.2.2', name: '3.5.1.2.2 设计', weight: 1 },
    { id: 'P3.5.1.2.3', name: '3.5.1.2.3 编码', weight: 1 },
    { id: 'P3.5.1.2.4', name: '3.5.1.2.4 测试', weight: 1 },
    { id: 'S3.5.3', name: '3.5.3 DevOps', weight: 3 },
    { id: 'SS3.5.2.1', name: '3.5.2.1 看板法介绍', weight: 2 },
    { id: 'SS3.5.2.2', name: '3.5.2.2 看板法的6个核心实践', weight: 2 },
    { id: 'SS3.5.2.3', name: '3.5.2.3 团队会议', weight: 2 },
    { id: 'P3.5.2.2.1', name: '3.5.2.2.1 可视化工作流', weight: 1 },
    { id: 'P3.5.2.2.2', name: '3.5.2.2.2 限制工作负荷', weight: 1 },
    { id: 'P3.5.2.2.3', name: '3.5.2.2.3 减少浪费', weight: 1 },
    { id: 'P3.5.2.2.4', name: '3.5.2.2.4 明确过程策略', weight: 1 },
    { id: 'P3.5.2.2.5', name: '3.5.2.2.5 创建反馈循环', weight: 1 },
    { id: 'P3.5.2.2.6', name: '3.5.2.2.6 变更中的相互合作', weight: 1 },
    { id: 'SS3.5.3.1', name: '3.5.3.1 DevOps介绍', weight: 2 },
    { id: 'SS3.5.3.2', name: '3.5.3.2 DevOps的5个持续循环阶段', weight: 2 },
    { id: 'P3.5.3.2.1', name: '3.5.3.2.1 持续开发', weight: 1 },
    { id: 'P3.5.3.2.2', name: '3.5.3.2.2 持续测试', weight: 1 },
    { id: 'P3.5.3.2.3', name: '3.5.3.2.3 持续集成', weight: 1 },
    { id: 'P3.5.3.2.4', name: '3.5.3.2.4 持续部署', weight: 1 },
    { id: 'P3.5.3.2.5', name: '3.5.3.2.5 持续监控', weight: 1 },
    { id: 'CH8', name: '第8章 需求建模——一种推荐的方法', weight: 5 },
    { id: 'T6.1', name: '6.1 核心原则', weight: 4 },
    { id: 'T6.2', name: '6.2 指导每个框架活动的原则', weight: 4 },
    { id: 'S6.1.1', name: '6.1.1 指导过程的原则', weight: 3 },
    { id: 'S6.1.2', name: '6.1.2 指导实践的原则', weight: 3 },
    { id: 'SS6.1.1.1', name: '6.1.1.1 介绍', weight: 2 },
    { id: 'SS6.1.1.2', name: '6.1.1.2 适用于通过过程框架的8个原则', weight: 2 },
    { id: 'P6.1.1.2.1', name: '6.1.1.2.1 原则1：敏捷', weight: 1 },
    { id: 'P6.1.1.2.2', name: '6.1.1.2.2 原则2：每一步都关注质量', weight: 1 },
    { id: 'P6.1.1.2.3', name: '6.1.1.2.3 原则3：做好适应的准备', weight: 1 },
    { id: 'P6.1.1.2.4', name: '6.1.1.2.4 原则4：建立一个有效的团队', weight: 1 },
    { id: 'P6.1.1.2.5', name: '6.1.1.2.5 原则5：建立沟通和协调机制', weight: 1 },
    { id: 'P6.1.1.2.6', name: '6.1.1.2.6 原则6：管理变更', weight: 1 },
    { id: 'P6.1.1.2.7', name: '6.1.1.2.7 原则7：评估风险', weight: 1 },
    { id: 'P6.1.1.2.8', name: '6.1.1.2.8 原则8：创造能给别人带来价值的工作产品', weight: 1 },
    { id: 'SS6.1.2.1', name: '6.1.2.1 介绍', weight: 2 },
    { id: 'SS6.1.2.2', name: '6.1.2.2 指导实践的8个原则', weight: 2 },
    { id: 'P6.1.2.2.1', name: '6.1.2.2.1 原则1：分治策略（分割和攻克）', weight: 1 },
    { id: 'P6.1.2.2.2', name: '6.1.2.2.2 原则2：理解抽象的使用', weight: 1 },
    { id: 'P6.1.2.2.3', name: '6.1.2.2.3 原则3：力求一致性', weight: 1 },
    { id: 'P6.1.2.2.4', name: '6.1.2.2.4 原则4：关注信息传送', weight: 1 },
    { id: 'P6.1.2.2.5', name: '6.1.2.2.5 原则5：构建能展示有效模块化的软件', weight: 1 },
    { id: 'P6.1.2.2.6', name: '6.1.2.2.6 原则6：寻找模型', weight: 1 },
    { id: 'P6.1.2.2.7', name: '6.1.2.2.7 原则7：在可能的时候，用大量不同的观点描述问题及其的解决办法', weight: 1 },
    { id: 'P6.1.2.2.8', name: '6.1.2.2.8 原则8：记住，有人将要对软件进行维护', weight: 1 },
    { id: 'T6.3', name: '6.3 小结', weight: 4 },
    { id: 'S6.2.1', name: '6.2.1 沟通原则', weight: 3 },
    { id: 'S6.2.2', name: '6.2.2 策划原则', weight: 3 },
    { id: 'SS6.2.1.1', name: '6.2.1.1 介绍', weight: 2 },
    { id: 'SS6.2.1.2', name: '6.2.1.2 沟通的10个原则', weight: 2 },
    { id: 'P6.2.1.2.1', name: '6.2.1.2.1 原则1：倾听', weight: 1 },
    { id: 'P6.2.1.2.2', name: '6.2.1.2.2原则2：有准备的沟通', weight: 1 },
    { id: 'P6.2.1.2.3', name: '6.2.1.2.3 原则3：沟通活动需要有人推动', weight: 1 },
    { id: 'P6.2.1.2.4', name: '6.2.1.2.4 原则4：最好当面沟通', weight: 1 },
    { id: 'P6.2.1.2.5', name: '6.2.1.2.5 原则5：记笔记并且记录所有决定', weight: 1 },
    { id: 'P6.2.1.2.6', name: '6.2.1.2.6 原则6：保持通力合作', weight: 1 },
    { id: 'P6.2.1.2.7', name: '6.2.1.2.7 原则7：把讨论集中在限定的范围内', weight: 1 },
    { id: 'P6.2.1.2.8', name: '6.2.1.2.8 原则8：如果某些东西很难表述清楚，就采用图形表示', weight: 1 },
    { id: 'P6.2.1.2.9', name: '6.2.1.2.9 原则9：敏捷地转换话题', weight: 1 },
    { id: 'P6.2.1.2.10', name: '6.2.1.2.10 原则10：协商不是一场竞赛或者一场游戏，双赢才能发挥协商的最大价值', weight: 1 },
    { id: 'S6.2.3', name: '6.2.3 建模原则', weight: 3 },
    { id: 'SS6.2.2.1', name: '6.2.2.1 介绍', weight: 2 },
    { id: 'SS6.2.2.2', name: '6.2.2.2 策划的10个原则', weight: 2 },
    { id: 'P6.2.2.2.1', name: '6.2.2.2.1 原则1：理解项目范围', weight: 1 },
    { id: 'P6.2.2.2.2', name: '6.2.2.2.2 原则2：让利益相关者参与策划', weight: 1 },
    { id: 'P6.2.2.2.3', name: '6.2.2.2.3 原则3：要认识道计划的指定应按照迭代方式进行', weight: 1 },
    { id: 'P6.2.2.2.4', name: '6.2.2.2.4 原则4：基于已知的估算', weight: 1 },
    { id: 'P6.2.2.2.5', name: '6.2.2.2.5 原则5：计划时考虑风险', weight: 1 },
    { id: 'P6.2.2.2.6', name: '6.2.2.2.6 原则6：保证可实现性', weight: 1 },
    { id: 'P6.2.2.2.7', name: '6.2.2.2.7 原则7：调整计划粒度', weight: 1 },
    { id: 'P6.2.2.2.8', name: '6.2.2.2.8 原则8：制定计划一确保质量', weight: 1 },
    { id: 'P6.2.2.2.9', name: '6.2.2.2.9 原则9：描述如何适应变化', weight: 1 },
    { id: 'P6.2.2.2.10', name: '6.2.2.2.10 原则10：经常跟踪并根据需要调整计划', weight: 1 },
    { id: 'S6.2.4', name: '6.2.4 构建原则', weight: 3 },
    { id: 'SS6.2.3.1', name: '6.2.3.1 介绍', weight: 2 },
    { id: 'SS6.2.3.2', name: '6.2.3.2 建模的10个原则', weight: 2 },
    { id: 'P6.2.3.2.1', name: '6.2.3.2.1 原则1：软件团队的主要目标是构建软件而不是创建模型', weight: 1 },
    { id: 'P6.2.3.2.2', name: '6.2.3.2.2 原则2：轻装前进——不要创建任何不需要的模型', weight: 1 },
    { id: 'P6.2.3.2.3', name: '6.2.3.2.3 原则3：尽量创建能描述问题和软件的最简单模型', weight: 1 },
    { id: 'P6.2.3.2.4', name: '6.2.3.2.4原则4：用能适应变化的方式构建模型', weight: 1 },
    { id: 'P6.2.3.2.5', name: '6.2.3.2.5 原则5：明确描述创建每一个模型的目的', weight: 1 },
    { id: 'P6.2.3.2.6', name: '6.2.3.2.6 原则6：调整模型来适应待开发系统', weight: 1 },
    { id: 'P6.2.3.2.7', name: '6.2.3.2.7 原则7：尽量构建有用的模型而不是完美的模型', weight: 1 },
    { id: 'P6.2.3.2.8', name: '6.2.3.2.8 原则8：对于模型的构造方法不要过于死板。', weight: 1 },
    { id: 'P6.2.3.2.9', name: '6.2.3.2.9 原则9：仔细注意模型', weight: 1 },
    { id: 'P6.2.3.2.10', name: '6.2.3.2.10 原则10：尽可能快地获得反馈', weight: 1 },
    { id: 'S6.2.5', name: '6.2.5 部署原则', weight: 3 },
    { id: 'SS6.2.4.1', name: '6.2.4.1 介绍', weight: 2 },
    { id: 'SS6.2.4.2', name: '6.2.4.2 编码原则', weight: 2 },
    { id: 'SS6.2.4.3', name: '6.2.4.3 测试原则', weight: 2 },
    { id: 'P6.2.4.2.1', name: '6.2.4.2.1 准备原则', weight: 1 },
    { id: 'P6.2.4.2.2', name: '6.2.4.2.2 编程原则', weight: 1 },
    { id: 'P6.2.4.2.3', name: '6.2.4.2.3 确认原则', weight: 1 },
    { id: 'P6.2.4.3.1', name: '6.2.4.3.1 介绍', weight: 1 },
    { id: 'P6.2.4.3.2', name: '6.2.4.3.2 原则1：所有的测试都应该可以追溯到用户需求', weight: 1 },
    { id: 'P6.2.4.3.3', name: '6.2.4.33 原则2：测试计划应该远在测试之前就开始着手', weight: 1 },
    { id: 'P6.2.4.3.4', name: '6.2.4.3.4 原则3：将Pareto原则应用于软件测试', weight: 1 },
    { id: 'P6.2.4.3.5', name: '6.2.4.3.5 原则4：测试应该从“微观”开始，逐步走向“宏观”', weight: 1 },
    { id: 'P6.2.4.3.6', name: '6.2.4.3.6 原则5：穷举测试是不可能的', weight: 1 },
    { id: 'P6.2.4.3.7', name: '6.2.4.3.7 原则6：为系统的每个模块做相应的缺陷密度测试', weight: 1 },
    { id: 'P6.2.4.3.8', name: '6.2.4.3.8 原则7：静态测试技术能得到很好的结果', weight: 1 },
    { id: 'P6.2.4.3.9', name: '6.2.4.3.9 原则8：跟踪缺陷，查找并测试未覆盖缺陷的模式', weight: 1 },
    { id: 'P6.2.4.3.10', name: '6.2.4.3.10 原则9：包含在演示软件中的测试用例是正确的行为', weight: 1 },
    { id: 'SS6.2.5.1', name: '6.2.5.1 介绍', weight: 2 },
    { id: 'SS6.2.5.2', name: '6.2.5.2 部署的5个原则', weight: 2 },
    { id: 'P6.2.5.2.1', name: '6.2.5.2.1 原则1：客户对于软件的期望必须得到管理', weight: 1 },
    { id: 'P6.2.5.2.2', name: '6.2.5.2.2 原则2：完整的交付包应该经过安装和测试', weight: 1 },
    { id: 'P6.2.5.2.3', name: '6.2.5.2.3 原则3：技术支持必须在软件交付之前就确定下来', weight: 1 },
    { id: 'P6.2.5.2.4', name: '6.2.5.2.4 原则4：必须为最终用户提供适当的说明材料', weight: 1 },
    { id: 'P6.2.5.2.5', name: '6.2.5.2.5 原则5：有缺陷的软件应该显改正再交付', weight: 1 },
    { id: 'CH15', name: '第15章 质量概念', weight: 5 },
    { id: 'T8.1', name: '8.1 需求分析', weight: 4 },
    { id: 'T8.2', name: '8.2 基于场景建模', weight: 4 },
    { id: 'S8.1.1', name: '8.1.1 总体目标和原理', weight: 3 },
    { id: 'S8.1.2', name: '8.1.2 分析的经验原则', weight: 3 },
    { id: 'SS8.1.1.1', name: '8.1.1.1 主要关注点', weight: 2 },
    { id: 'SS8.1.1.2', name: '8.1.1.2 三个主要目标', weight: 2 },
    { id: 'S8.1.3', name: '8.1.3 需求建模原则', weight: 3 },
    { id: 'SS8.1.2.1', name: '8.1.2.1 模型关注可见需求', weight: 2 },
    { id: 'SS8.1.2.2', name: '8.1.2.2 模型元素存在即有用', weight: 2 },
    { id: 'SS8.1.2.3', name: '8.1.2.3 基础结构和非功能模型暂缓考虑', weight: 2 },
    { id: 'SS8.1.2.4', name: '8.1.2.4 最小化整个系统内联', weight: 2 },
    { id: 'SS8.1.2.5', name: '8.1.2.5 确认需求模型为所有利益相关者都带来价值', weight: 2 },
    { id: 'SS8.1.2.6', name: '8.1.2.6 保持模型简洁', weight: 2 },
    { id: 'SS8.1.3.1', name: '8.1.3.1 原则1：问题的信息域必须得到表达和理解', weight: 2 },
    { id: 'SS8.1.3.2', name: '8.1.3.2 原则2：必须定义软件执行的功能', weight: 2 },
    { id: 'SS8.1.3.3', name: '8.1.3.3 原则3：必须表示软件的行为', weight: 2 },
    { id: 'SS8.1.3.4', name: '8.1.3.4 原则4：描述信息、功能和行为的模型必须以分层的方式进行分割以揭示细节', weight: 2 },
    { id: 'SS8.1.3.5', name: '8.1.3.5 原则5：分析任务应从基本信息转向实现细节', weight: 2 },
    { id: 'T8.3', name: '8.3 基于类建模', weight: 4 },
    { id: 'S8.2.1', name: '8.2.1 参与者和用户概要文件', weight: 3 },
    { id: 'S8.2.2', name: '8.2.2 创建用例', weight: 3 },
    { id: 'SS8.2.1.1', name: '8.2.1.1 参与者', weight: 2 },
    { id: 'SS8.2.1.2', name: '8.2.1.2 用户概要文件', weight: 2 },
    { id: 'S8.2.3', name: '8.2.3 编写用例', weight: 3 },
    { id: 'SS8.2.2.1', name: '8.2.2.1 用例的定义', weight: 2 },
    { id: 'SS8.2.2.2', name: '8.2.2.2 创建用例的疑问', weight: 2 },
    { id: 'P8.2.2.2.1', name: '8.2.2.2.1 编写什么？ ', weight: 1 },
    { id: 'P8.2.2.2.2', name: '8.2.2.2.2 写多少？', weight: 1 },
    { id: 'P8.2.2.2.3', name: '8.2.2.2.3 编写说明应该有多详细？', weight: 1 },
    { id: 'P8.2.2.2.4', name: '8.2.2.2.4 如何组织说明？', weight: 1 },
    { id: 'SS8.2.3.1', name: '8.2.3.1 为什么需要正式的用例描述？', weight: 2 },
    { id: 'SS8.2.3.2', name: '8.2.3.2 SafeHome监视的用例模板中包含的关键元素', weight: 2 },
    { id: 'SS8.2.3.3', name: '8.2.3.3 图形化用户场景', weight: 2 },
    { id: 'T8.4', name: '8.4 功能建模', weight: 4 },
    { id: 'S8.3.1', name: '8.3.1 识别分析类', weight: 3 },
    { id: 'S8.3.2', name: '8.3.2 定义属性和操作', weight: 3 },
    { id: 'SS8.3.1.1', name: '8.3.1.1 识别类', weight: 2 },
    { id: 'SS8.3.1.2', name: '8.3.1.2 分析类——寻找潜在类', weight: 2 },
    { id: 'S8.3.3', name: '8.3.3 UML类模型', weight: 3 },
    { id: 'SS8.3.2.1', name: '8.3.2.1 属性定义', weight: 2 },
    { id: 'SS8.3.2.2', name: '8.3.2.2 操作定义', weight: 2 },
    { id: 'S8.3.4', name: '8.3.4 类–职责–协作者建模', weight: 3 },
    { id: 'SS8.3.4.1', name: '8.3.4.1 模型介绍', weight: 2 },
    { id: 'SS8.3.4.2', name: '8.3.4.2 拓展类的三种分类方式', weight: 2 },
    { id: 'SS8.3.4.3', name: '8.3.4.3 职责的5个指导原则', weight: 2 },
    { id: 'SS8.3.4.4', name: '8.3.4.4 协作的必要性', weight: 2 },
    { id: 'P8.3.4.3.1', name: '8.3.4.3.1 智能系统应分布在所有类中以求最佳地满足问题的需求', weight: 1 },
    { id: 'P8.3.4.3.2', name: '8.3.4.3.2 每个职责的说明应尽可能具有普遍性', weight: 1 },
    { id: 'P8.3.4.3.3', name: '8.3.4.3.3 信息和与之相关的行为应放在同一个类中', weight: 1 },
    { id: 'P8.3.4.3.4', name: '8.3.4.3.4 某个事物的信息应局限于一个类中而不要分布在多个类中', weight: 1 },
    { id: 'P8.3.4.3.5', name: '8.3.4.3.5 职责应由相关类共享', weight: 1 },
    { id: 'SS8.3.4.5', name: '8.3.4.5 评审模型', weight: 2 },
    { id: 'T8.5', name: '8.5 行为建模', weight: 4 },
    { id: 'S8.4.1', name: '8.4.1 介绍', weight: 3 },
    { id: 'S8.4.2', name: '8.4.2 过程视图', weight: 3 },
    { id: 'S8.4.3', name: '8.4.3 UML顺序图', weight: 3 },
    { id: 'T8.6', name: '8.6 小结', weight: 4 },
    { id: 'S8.5.1', name: '8.5.1 介绍', weight: 3 },
    { id: 'S8.5.2', name: '8.5.2 识别用例事件', weight: 3 },
    { id: 'S8.5.3', name: '8.5.3 UML状态图', weight: 3 },
    { id: 'S8.5.4', name: '8.5.4 UML活动图', weight: 3 },
    { id: 'SS8.5.4.1', name: '8.5.4.1 UML活动图的作用', weight: 2 },
    { id: 'SS8.5.4.2', name: '8.5.4.2 UML泳道图的应用', weight: 2 },
    { id: 'T15.1', name: '15.1 什么是质量', weight: 4 },
    { id: 'T15.2', name: '15.2 软件质量', weight: 4 },
    { id: 'S15.1.1', name: '15.1.1 David-Garvin关于质量的5个观点', weight: 3 },
    { id: 'S15.1.2', name: '15.1.2 设计质量和符合质量', weight: 3 },
    { id: 'SS15.1.1.1', name: '15.1.1.1 先验论观点', weight: 2 },
    { id: 'SS15.1.1.2', name: '15.1.1.2 用户观点', weight: 2 },
    { id: 'SS15.1.1.3', name: '15.1.1.3 制造商观点', weight: 2 },
    { id: 'SS15.1.1.4', name: '15.1.1.4 产品观点', weight: 2 },
    { id: 'SS15.1.1.5', name: '15.1.1.5 基于价值的观点', weight: 2 },
    { id: 'S15.1.3', name: '15.1.3 质量之外', weight: 3 },
    { id: 'SS15.1.2.1', name: '15.1.2.1 设计质量', weight: 2 },
    { id: 'SS15.1.2.2', name: '15.1.2.2 符合质量', weight: 2 },
    { id: 'T15.3', name: '15.3 软件质量困境', weight: 4 },
    { id: 'S15.2.1', name: '15.2.1 软件质量的定义', weight: 3 },
    { id: 'S15.2.2', name: '15.2.2 质量因素', weight: 3 },
    { id: 'SS15.2.1.1', name: '15.2.1.1 有效地软件过程', weight: 2 },
    { id: 'SS15.2.1.2', name: '15.2.1.2 有用的产品', weight: 2 },
    { id: 'SS15.2.1.3', name: '15.2.1.3 为软件产品的生产者和使用者带来增值', weight: 2 },
    { id: 'S15.2.3', name: '15.2.3 定性质量评估', weight: 3 },
    { id: 'SS15.2.2.1', name: '15.2.2.1 McCall的软件质量因素', weight: 2 },
    { id: 'SS15.2.2.2', name: '15.2.2.2 ISO 9126质量因素', weight: 2 },
    { id: 'P15.2.2.1.1', name: '15.2.2.1.1 操作特性 (产品运行)', weight: 1 },
    { id: 'P15.2.2.1.2', name: '15.2.2.1.2 承受变更的能力 (产品修改)', weight: 1 },
    { id: 'P15.2.2.1.3', name: '15.2.2.1.3 对新环境的适应能力 (产品转移)', weight: 1 },
    { id: 'SS15.2.2.3', name: '15.2.2.3 使用质量模型', weight: 2 },
    { id: 'SS15.2.2.4', name: '15.2.2.4 产品质量模型', weight: 2 },
    { id: 'S15.2.4', name: '15.2.4 定量质量评估', weight: 3 },
    { id: 'T15.4', name: '15.4 实现软件质量', weight: 4 },
    { id: 'S15.3.1', name: '15.3.1 困境论述', weight: 3 },
    { id: 'S15.3.2', name: '15.3.2 “足够好”的软件', weight: 3 },
    { id: 'S15.3.3', name: '15.3.3 质量的成本', weight: 3 },
    { id: 'S15.3.4', name: '15.3.4 风险', weight: 3 },
    { id: 'SS15.3.3.1', name: '15.3.3.1 质量成本的争论', weight: 2 },
    { id: 'SS15.3.3.2', name: '15.3.3.2 质量成本的3个分类', weight: 2 },
    { id: 'P15.3.3.2.1', name: '15.3.3.2.1 预防成本', weight: 1 },
    { id: 'P15.3.3.2.2', name: '15.3.3.2.2 评估成本', weight: 1 },
    { id: 'P15.3.3.2.3', name: '15.3.3.2.3 失效成本', weight: 1 },
    { id: 'S15.3.5', name: '15.3.5 疏忽和责任', weight: 3 },
    { id: 'SS15.3.4.1', name: '15.3.4.1 低质量软件带来风险', weight: 2 },
    { id: 'SS15.3.4.2', name: '15.3.4.2 一个极端的例子与警示', weight: 2 },
    { id: 'S15.3.6', name: '15.3.6 质量和安全', weight: 3 },
    { id: 'S15.3.7', name: '15.3.7 管理活动的影响', weight: 3 },
    { id: 'SS15.3.6.1', name: '15.3.6.1 质量和安全的关系', weight: 2 },
    { id: 'SS15.3.6.2', name: '15.3.6.2 两种类型的软件问题', weight: 2 },
    { id: 'SS15.3.7.1', name: '15.3.7.1 质量受到管理活动影响', weight: 2 },
    { id: 'SS15.3.7.2', name: '15.3.7.2 三种决策', weight: 2 },
    { id: 'P15.3.7.2.1', name: '15.3.7.2.1 估算决策', weight: 1 },
    { id: 'P15.3.7.2.2', name: '15.3.7.2.2 进度安排决策', weight: 1 },
    { id: 'P15.3.7.2.3', name: '15.3.7.2.3 面对风险的决策', weight: 1 },
    { id: 'T15.5', name: '15.5 小结', weight: 4 },
    { id: 'S15.4.1', name: '15.4.1 实现高质量软件的四大管理和实践活动', weight: 3 },
    { id: 'S15.4.2', name: '15.4.2 机器学习和缺陷预测', weight: 3 },
    { id: 'SS15.4.1.1', name: '15.4.1.1 软件工程方法 ', weight: 2 },
    { id: 'SS15.4.1.2', name: '15.4.1.2 项目管理技术', weight: 2 },
    { id: 'SS15.4.1.3', name: '15.4.1.3 质量控制', weight: 2 },
    { id: 'SS15.4.1.4', name: '15.4.1.4 质量保证', weight: 2 },
    { id: 'SS1.1.2.1', name: '1.1.2.1 计算机软件的7类应用', weight: 2 },
    { id: 'SS1.2.2.1', name: '1.2.2.1 软件工程层次', weight: 2 },
    { id: 'SS1.3.1.1', name: '1.3.1.1 通用的5个框架活动', weight: 2 },
    { id: 'SS1.3.2.1', name: '1.3.2.1 典型的普适性活动', weight: 2 },
    { id: 'SS1.4.2.1', name: '1.4.2.1 David Hooker的7个关注软件工程整体实践原则', weight: 2 },
    { id: 'S1.5.1', name: '1.5.1 软工项目来自业务需求', weight: 3 }
];
     this.tempEdges = [{
          "id": 1,
          "source": "CH1",
          "target": "CH3",
          "relation": "Next_SB",
          "value": 1
      },
      {
          "id": 2,
          "source": "T1.1",
          "target": "T1.2",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 3,
          "source": "S1.1.1",
          "target": "S1.1.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 4,
          "source": "SS1.1.1.1",
          "target": "SS1.1.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 5,
          "source": "SS1.1.1.2",
          "target": "SS1.1.1.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 6,
          "source": "P1.1.1.3.1",
          "target": "P1.1.1.3.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 7,
          "source": "P1.1.1.3.2",
          "target": "P1.1.1.3.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 8,
          "source": "S1.1.2",
          "target": "S1.1.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 9,
          "source": "P1.1.2.1.1",
          "target": "P1.1.2.1.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 10,
          "source": "P1.1.2.1.2",
          "target": "P1.1.2.1.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 11,
          "source": "P1.1.2.1.3",
          "target": "P1.1.2.1.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 12,
          "source": "P1.1.2.1.4",
          "target": "P1.1.2.1.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 13,
          "source": "P1.1.2.1.5",
          "target": "P1.1.2.1.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 14,
          "source": "P1.1.2.1.6",
          "target": "P1.1.2.1.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 15,
          "source": "SS1.1.3.1",
          "target": "SS1.1.3.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 16,
          "source": "SS1.1.3.2",
          "target": "SS1.1.3.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 17,
          "source": "T1.2",
          "target": "T1.3",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 18,
          "source": "S1.2.1",
          "target": "S1.2.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 19,
          "source": "P1.2.2.1.1",
          "target": "P1.2.2.1.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 20,
          "source": "P1.2.2.1.2",
          "target": "P1.2.2.1.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 21,
          "source": "T1.3",
          "target": "T1.4",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 22,
          "source": "S1.3.1",
          "target": "S1.3.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 23,
          "source": "P1.3.1.1.1",
          "target": "P1.3.1.1.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 24,
          "source": "P1.3.1.1.2",
          "target": "P1.3.1.1.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 25,
          "source": "P1.3.1.1.3",
          "target": "P1.3.1.1.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 26,
          "source": "P1.3.1.1.4",
          "target": "P1.3.1.1.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 27,
          "source": "S1.3.2",
          "target": "S1.3.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 28,
          "source": "P1.3.2.1.1",
          "target": "P1.3.2.1.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 29,
          "source": "P1.3.2.1.2",
          "target": "P1.3.2.1.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 30,
          "source": "P1.3.2.1.3",
          "target": "P1.3.2.1.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 31,
          "source": "P1.3.2.1.4",
          "target": "P1.3.2.1.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 32,
          "source": "P1.3.2.1.5",
          "target": "P1.3.2.1.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 33,
          "source": "P1.3.2.1.6",
          "target": "P1.3.2.1.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 34,
          "source": "P1.3.2.1.7",
          "target": "P1.3.2.1.8",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 35,
          "source": "T1.4",
          "target": "T1.5",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 36,
          "source": "S1.4.1",
          "target": "S1.4.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 37,
          "source": "SS1.4.1.1",
          "target": "SS1.4.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 38,
          "source": "SS1.4.1.2",
          "target": "SS1.4.1.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 39,
          "source": "SS1.4.1.3",
          "target": "SS1.4.1.4",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 40,
          "source": "P1.4.2.1.1",
          "target": "P1.4.2.1.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 41,
          "source": "P1.4.2.1.2",
          "target": "P1.4.2.1.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 42,
          "source": "P1.4.2.1.3",
          "target": "P1.4.2.1.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 43,
          "source": "P1.4.2.1.4",
          "target": "P1.4.2.1.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 44,
          "source": "P1.4.2.1.5",
          "target": "P1.4.2.1.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 45,
          "source": "P1.4.2.1.6",
          "target": "P1.4.2.1.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 46,
          "source": "T1.5",
          "target": "T1.6",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 47,
          "source": "CH3",
          "target": "CH6",
          "relation": "Next_SB",
          "value": 1
      },
      {
          "id": 48,
          "source": "T3.1",
          "target": "T3.2",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 49,
          "source": "S3.1.1",
          "target": "S3.1.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 50,
          "source": "S3.1.2",
          "target": "S3.1.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 51,
          "source": "S3.1.2.1",
          "target": "S3.1.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 52,
          "source": "S3.1.2.2",
          "target": "S3.1.2.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 53,
          "source": "S3.1.2.3",
          "target": "S3.1.2.4",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 54,
          "source": "S3.1.2.4",
          "target": "S3.1.2.5",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 55,
          "source": "S3.1.3",
          "target": "S3.1.4",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 56,
          "source": "SS3.1.4.1",
          "target": "SS3.1.4.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 57,
          "source": "T3.2",
          "target": "T3.3",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 58,
          "source": "S3.2.1",
          "target": "S3.2.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 59,
          "source": "T3.3",
          "target": "T3.4",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 60,
          "source": "S3.3.1",
          "target": "S3.3.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 61,
          "source": "S3.3.2",
          "target": "S3.3.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 62,
          "source": "SS3.3.2.1",
          "target": "SS3.3.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 63,
          "source": "SS3.3.3.1",
          "target": "SS3.3.3.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 64,
          "source": "P3.3.3.2.1",
          "target": "P3.3.3.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 65,
          "source": "P3.3.3.2.2",
          "target": "P3.3.3.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 66,
          "source": "P3.3.3.2.3",
          "target": "P3.3.3.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 67,
          "source": "P3.3.3.2.4",
          "target": "P3.3.3.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 68,
          "source": "P3.3.3.2.5",
          "target": "P3.3.3.2.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 69,
          "source": "P3.3.3.2.6",
          "target": "P3.3.3.2.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 70,
          "source": "T3.4",
          "target": "T3.5",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 71,
          "source": "S3.4.1",
          "target": "S3.4.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 72,
          "source": "S3.4.2",
          "target": "S3.4.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 73,
          "source": "S3.4.3",
          "target": "S3.4.4",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 74,
          "source": "S3.4.4",
          "target": "S3.4.5",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 75,
          "source": "T3.5",
          "target": "T3.6",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 76,
          "source": "S3.5.1",
          "target": "S3.5.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 77,
          "source": "SS3.5.1.1",
          "target": "SS3.5.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 78,
          "source": "P3.5.1.2.1",
          "target": "P3.5.1.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 79,
          "source": "P3.5.1.2.2",
          "target": "P3.5.1.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 80,
          "source": "P3.5.1.2.3",
          "target": "P3.5.1.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 81,
          "source": "S3.5.2",
          "target": "S3.5.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 82,
          "source": "SS3.5.2.1",
          "target": "SS3.5.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 83,
          "source": "SS3.5.2.2",
          "target": "SS3.5.2.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 84,
          "source": "P3.5.2.2.1",
          "target": "P3.5.2.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 85,
          "source": "P3.5.2.2.2",
          "target": "P3.5.2.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 86,
          "source": "P3.5.2.2.3",
          "target": "P3.5.2.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 87,
          "source": "P3.5.2.2.4",
          "target": "P3.5.2.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 88,
          "source": "P3.5.2.2.5",
          "target": "P3.5.2.2.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 89,
          "source": "SS3.5.3.1",
          "target": "SS3.5.3.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 90,
          "source": "P3.5.3.2.1",
          "target": "P3.5.3.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 91,
          "source": "P3.5.3.2.2",
          "target": "P3.5.3.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 92,
          "source": "P3.5.3.2.3",
          "target": "P3.5.3.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 93,
          "source": "P3.5.3.2.4",
          "target": "P3.5.3.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 94,
          "source": "CH6",
          "target": "CH8",
          "relation": "Next_SB",
          "value": 1
      },
      {
          "id": 95,
          "source": "T6.1",
          "target": "T6.2",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 96,
          "source": "S6.1.1",
          "target": "S6.1.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 97,
          "source": "SS6.1.1.1",
          "target": "SS6.1.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 98,
          "source": "P6.1.1.2.1",
          "target": "P6.1.1.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 99,
          "source": "P6.1.1.2.2",
          "target": "P6.1.1.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 100,
          "source": "P6.1.1.2.3",
          "target": "P6.1.1.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 101,
          "source": "P6.1.1.2.4",
          "target": "P6.1.1.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 102,
          "source": "P6.1.1.2.5",
          "target": "P6.1.1.2.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 103,
          "source": "P6.1.1.2.6",
          "target": "P6.1.1.2.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 104,
          "source": "P6.1.1.2.7",
          "target": "P6.1.1.2.8",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 105,
          "source": "SS6.1.2.1",
          "target": "SS6.1.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 106,
          "source": "P6.1.2.2.1",
          "target": "P6.1.2.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 107,
          "source": "P6.1.2.2.2",
          "target": "P6.1.2.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 108,
          "source": "P6.1.2.2.3",
          "target": "P6.1.2.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 109,
          "source": "P6.1.2.2.4",
          "target": "P6.1.2.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 110,
          "source": "P6.1.2.2.5",
          "target": "P6.1.2.2.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 111,
          "source": "P6.1.2.2.6",
          "target": "P6.1.2.2.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 112,
          "source": "P6.1.2.2.7",
          "target": "P6.1.2.2.8",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 113,
          "source": "T6.2",
          "target": "T6.3",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 114,
          "source": "S6.2.1",
          "target": "S6.2.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 115,
          "source": "SS6.2.1.1",
          "target": "SS6.2.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 116,
          "source": "P6.2.1.2.1",
          "target": "P6.2.1.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 117,
          "source": "P6.2.1.2.2",
          "target": "P6.2.1.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 118,
          "source": "P6.2.1.2.3",
          "target": "P6.2.1.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 119,
          "source": "P6.2.1.2.4",
          "target": "P6.2.1.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 120,
          "source": "P6.2.1.2.5",
          "target": "P6.2.1.2.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 121,
          "source": "P6.2.1.2.6",
          "target": "P6.2.1.2.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 122,
          "source": "P6.2.1.2.7",
          "target": "P6.2.1.2.8",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 123,
          "source": "P6.2.1.2.8",
          "target": "P6.2.1.2.9",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 124,
          "source": "P6.2.1.2.9",
          "target": "P6.2.1.2.10",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 125,
          "source": "S6.2.2",
          "target": "S6.2.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 126,
          "source": "SS6.2.2.1",
          "target": "SS6.2.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 127,
          "source": "P6.2.2.2.1",
          "target": "P6.2.2.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 128,
          "source": "P6.2.2.2.2",
          "target": "P6.2.2.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 129,
          "source": "P6.2.2.2.3",
          "target": "P6.2.2.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 130,
          "source": "P6.2.2.2.4",
          "target": "P6.2.2.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 131,
          "source": "P6.2.2.2.5",
          "target": "P6.2.2.2.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 132,
          "source": "P6.2.2.2.6",
          "target": "P6.2.2.2.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 133,
          "source": "P6.2.2.2.7",
          "target": "P6.2.2.2.8",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 134,
          "source": "P6.2.2.2.8",
          "target": "P6.2.2.2.9",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 135,
          "source": "P6.2.2.2.9",
          "target": "P6.2.2.2.10",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 136,
          "source": "S6.2.3",
          "target": "S6.2.4",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 137,
          "source": "SS6.2.3.1",
          "target": "SS6.2.3.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 138,
          "source": "P6.2.3.2.1",
          "target": "P6.2.3.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 139,
          "source": "P6.2.3.2.2",
          "target": "P6.2.3.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 140,
          "source": "P6.2.3.2.3",
          "target": "P6.2.3.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 141,
          "source": "P6.2.3.2.4",
          "target": "P6.2.3.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 142,
          "source": "P6.2.3.2.5",
          "target": "P6.2.3.2.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 143,
          "source": "P6.2.3.2.6",
          "target": "P6.2.3.2.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 144,
          "source": "P6.2.3.2.7",
          "target": "P6.2.3.2.8",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 145,
          "source": "P6.2.3.2.8",
          "target": "P6.2.3.2.9",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 146,
          "source": "P6.2.3.2.9",
          "target": "P6.2.3.2.10",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 147,
          "source": "S6.2.4",
          "target": "S6.2.5",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 148,
          "source": "SS6.2.4.1",
          "target": "SS6.2.4.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 149,
          "source": "SS6.2.4.2",
          "target": "SS6.2.4.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 150,
          "source": "P6.2.4.2.1",
          "target": "P6.2.4.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 151,
          "source": "P6.2.4.2.2",
          "target": "P6.2.4.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 152,
          "source": "P6.2.4.3.1",
          "target": "P6.2.4.3.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 153,
          "source": "P6.2.4.3.2",
          "target": "P6.2.4.3.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 154,
          "source": "P6.2.4.3.3",
          "target": "P6.2.4.3.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 155,
          "source": "P6.2.4.3.4",
          "target": "P6.2.4.3.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 156,
          "source": "P6.2.4.3.5",
          "target": "P6.2.4.3.6",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 157,
          "source": "P6.2.4.3.6",
          "target": "P6.2.4.3.7",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 158,
          "source": "P6.2.4.3.7",
          "target": "P6.2.4.3.8",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 159,
          "source": "P6.2.4.3.8",
          "target": "P6.2.4.3.9",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 160,
          "source": "P6.2.4.3.9",
          "target": "P6.2.4.3.10",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 161,
          "source": "SS6.2.5.1",
          "target": "SS6.2.5.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 162,
          "source": "P6.2.5.2.1",
          "target": "P6.2.5.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 163,
          "source": "P6.2.5.2.2",
          "target": "P6.2.5.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 164,
          "source": "P6.2.5.2.3",
          "target": "P6.2.5.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 165,
          "source": "P6.2.5.2.4",
          "target": "P6.2.5.2.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 166,
          "source": "CH8",
          "target": "CH15",
          "relation": "Next_SB",
          "value": 1
      },
      {
          "id": 167,
          "source": "T8.1",
          "target": "T8.2",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 168,
          "source": "S8.1.1",
          "target": "S8.1.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 169,
          "source": "SS8.1.1.1",
          "target": "SS8.1.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 170,
          "source": "S8.1.2",
          "target": "S8.1.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 171,
          "source": "SS8.1.2.1",
          "target": "SS8.1.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 172,
          "source": "SS8.1.2.2",
          "target": "SS8.1.2.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 173,
          "source": "SS8.1.2.3",
          "target": "SS8.1.2.4",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 174,
          "source": "SS8.1.2.4",
          "target": "SS8.1.2.5",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 175,
          "source": "SS8.1.2.5",
          "target": "SS8.1.2.6",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 176,
          "source": "SS8.1.3.1",
          "target": "SS8.1.3.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 177,
          "source": "SS8.1.3.2",
          "target": "SS8.1.3.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 178,
          "source": "SS8.1.3.3",
          "target": "SS8.1.3.4",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 179,
          "source": "SS8.1.3.4",
          "target": "SS8.1.3.5",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 180,
          "source": "T8.2",
          "target": "T8.3",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 181,
          "source": "S8.2.1",
          "target": "S8.2.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 182,
          "source": "SS8.2.1.1",
          "target": "SS8.2.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 183,
          "source": "S8.2.2",
          "target": "S8.2.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 184,
          "source": "SS8.2.2.1",
          "target": "SS8.2.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 185,
          "source": "P8.2.2.2.1",
          "target": "P8.2.2.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 186,
          "source": "P8.2.2.2.2",
          "target": "P8.2.2.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 187,
          "source": "P8.2.2.2.3",
          "target": "P8.2.2.2.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 188,
          "source": "SS8.2.3.1",
          "target": "SS8.2.3.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 189,
          "source": "SS8.2.3.2",
          "target": "SS8.2.3.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 190,
          "source": "T8.3",
          "target": "T8.4",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 191,
          "source": "S8.3.1",
          "target": "S8.3.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 192,
          "source": "SS8.3.1.1",
          "target": "SS8.3.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 193,
          "source": "S8.3.2",
          "target": "S8.3.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 194,
          "source": "SS8.3.2.1",
          "target": "SS8.3.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 195,
          "source": "S8.3.3",
          "target": "S8.3.4",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 196,
          "source": "SS8.3.4.1",
          "target": "SS8.3.4.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 197,
          "source": "SS8.3.4.2",
          "target": "SS8.3.4.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 198,
          "source": "SS8.3.4.3",
          "target": "SS8.3.4.4",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 199,
          "source": "P8.3.4.3.1",
          "target": "P8.3.4.3.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 200,
          "source": "P8.3.4.3.2",
          "target": "P8.3.4.3.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 201,
          "source": "P8.3.4.3.3",
          "target": "P8.3.4.3.4",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 202,
          "source": "P8.3.4.3.4",
          "target": "P8.3.4.3.5",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 203,
          "source": "SS8.3.4.4",
          "target": "SS8.3.4.5",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 204,
          "source": "T8.4",
          "target": "T8.5",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 205,
          "source": "S8.4.1",
          "target": "S8.4.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 206,
          "source": "S8.4.2",
          "target": "S8.4.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 207,
          "source": "T8.5",
          "target": "T8.6",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 208,
          "source": "S8.5.1",
          "target": "S8.5.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 209,
          "source": "S8.5.2",
          "target": "S8.5.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 210,
          "source": "S8.5.3",
          "target": "S8.5.4",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 211,
          "source": "SS8.5.4.1",
          "target": "SS8.5.4.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 212,
          "source": "T15.1",
          "target": "T15.2",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 213,
          "source": "S15.1.1",
          "target": "S15.1.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 214,
          "source": "SS15.1.1.1",
          "target": "SS15.1.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 215,
          "source": "SS15.1.1.2",
          "target": "SS15.1.1.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 216,
          "source": "SS15.1.1.3",
          "target": "SS15.1.1.4",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 217,
          "source": "SS15.1.1.4",
          "target": "SS15.1.1.5",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 218,
          "source": "S15.1.2",
          "target": "S15.1.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 219,
          "source": "SS15.1.2.1",
          "target": "SS15.1.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 220,
          "source": "T15.2",
          "target": "T15.3",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 221,
          "source": "S15.2.1",
          "target": "S15.2.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 222,
          "source": "SS15.2.1.1",
          "target": "SS15.2.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 223,
          "source": "SS15.2.1.2",
          "target": "SS15.2.1.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 224,
          "source": "S15.2.2",
          "target": "S15.2.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 225,
          "source": "SS15.2.2.1",
          "target": "SS15.2.2.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 226,
          "source": "P15.2.2.1.1",
          "target": "P15.2.2.1.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 227,
          "source": "P15.2.2.1.2",
          "target": "P15.2.2.1.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 228,
          "source": "SS15.2.2.2",
          "target": "SS15.2.2.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 229,
          "source": "SS15.2.2.3",
          "target": "SS15.2.2.4",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 230,
          "source": "S15.2.3",
          "target": "S15.2.4",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 231,
          "source": "T15.3",
          "target": "T15.4",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 232,
          "source": "S15.3.1",
          "target": "S15.3.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 233,
          "source": "S15.3.2",
          "target": "S15.3.3",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 234,
          "source": "S15.3.3",
          "target": "S15.3.4",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 235,
          "source": "SS15.3.3.1",
          "target": "SS15.3.3.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 236,
          "source": "P15.3.3.2.1",
          "target": "P15.3.3.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 237,
          "source": "P15.3.3.2.2",
          "target": "P15.3.3.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 238,
          "source": "S15.3.4",
          "target": "S15.3.5",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 239,
          "source": "SS15.3.4.1",
          "target": "SS15.3.4.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 240,
          "source": "S15.3.5",
          "target": "S15.3.6",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 241,
          "source": "S15.3.6",
          "target": "S15.3.7",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 242,
          "source": "SS15.3.6.1",
          "target": "SS15.3.6.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 243,
          "source": "SS15.3.7.1",
          "target": "SS15.3.7.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 244,
          "source": "P15.3.7.2.1",
          "target": "P15.3.7.2.2",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 245,
          "source": "P15.3.7.2.2",
          "target": "P15.3.7.2.3",
          "relation": "Next_P",
          "value": 1
      },
      {
          "id": 246,
          "source": "T15.4",
          "target": "T15.5",
          "relation": "Next_TP",
          "value": 1
      },
      {
          "id": 247,
          "source": "S15.4.1",
          "target": "S15.4.2",
          "relation": "Next_ST",
          "value": 1
      },
      {
          "id": 248,
          "source": "SS15.4.1.1",
          "target": "SS15.4.1.2",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 249,
          "source": "SS15.4.1.2",
          "target": "SS15.4.1.3",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 250,
          "source": "SS15.4.1.3",
          "target": "SS15.4.1.4",
          "relation": "Next_SS",
          "value": 1
      },
      {
          "id": 251,
          "source": "T1.1",
          "target": "CH1",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 252,
          "source": "S1.1.1",
          "target": "T1.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 253,
          "source": "SS1.1.1.1",
          "target": "S1.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 254,
          "source": "SS1.1.1.2",
          "target": "S1.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 255,
          "source": "SS1.1.1.3",
          "target": "S1.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 256,
          "source": "P1.1.1.3.1",
          "target": "SS1.1.1.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 257,
          "source": "P1.1.1.3.2",
          "target": "SS1.1.1.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 258,
          "source": "P1.1.1.3.3",
          "target": "SS1.1.1.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 259,
          "source": "S1.1.2",
          "target": "T1.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 260,
          "source": "SS1.1.2.1",
          "target": "S1.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 261,
          "source": "P1.1.2.1.1",
          "target": "SS1.1.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 262,
          "source": "P1.1.2.1.2",
          "target": "SS1.1.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 263,
          "source": "P1.1.2.1.3",
          "target": "SS1.1.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 264,
          "source": "P1.1.2.1.4",
          "target": "SS1.1.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 265,
          "source": "P1.1.2.1.5",
          "target": "SS1.1.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 266,
          "source": "P1.1.2.1.6",
          "target": "SS1.1.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 267,
          "source": "P1.1.2.1.7",
          "target": "SS1.1.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 268,
          "source": "S1.1.3",
          "target": "T1.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 269,
          "source": "SS1.1.3.1",
          "target": "S1.1.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 270,
          "source": "SS1.1.3.2",
          "target": "S1.1.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 271,
          "source": "SS1.1.3.3",
          "target": "S1.1.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 272,
          "source": "T1.2",
          "target": "CH1",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 273,
          "source": "S1.2.1",
          "target": "T1.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 274,
          "source": "S1.2.2",
          "target": "T1.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 275,
          "source": "SS1.2.2.1",
          "target": "S1.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 276,
          "source": "P1.2.2.1.1",
          "target": "SS1.2.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 277,
          "source": "P1.2.2.1.2",
          "target": "SS1.2.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 278,
          "source": "P1.2.2.1.3",
          "target": "SS1.2.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 279,
          "source": "T1.3",
          "target": "CH1",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 280,
          "source": "S1.3.1",
          "target": "T1.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 281,
          "source": "SS1.3.1.1",
          "target": "S1.3.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 282,
          "source": "P1.3.1.1.1",
          "target": "SS1.3.1.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 283,
          "source": "P1.3.1.1.2",
          "target": "SS1.3.1.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 284,
          "source": "P1.3.1.1.3",
          "target": "SS1.3.1.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 285,
          "source": "P1.3.1.1.4",
          "target": "SS1.3.1.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 286,
          "source": "P1.3.1.1.5",
          "target": "SS1.3.1.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 287,
          "source": "S1.3.2",
          "target": "T1.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 288,
          "source": "SS1.3.2.1",
          "target": "S1.3.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 289,
          "source": "P1.3.2.1.1",
          "target": "SS1.3.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 290,
          "source": "P1.3.2.1.2",
          "target": "SS1.3.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 291,
          "source": "P1.3.2.1.3",
          "target": "SS1.3.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 292,
          "source": "P1.3.2.1.4",
          "target": "SS1.3.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 293,
          "source": "P1.3.2.1.5",
          "target": "SS1.3.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 294,
          "source": "P1.3.2.1.6",
          "target": "SS1.3.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 295,
          "source": "P1.3.2.1.7",
          "target": "SS1.3.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 296,
          "source": "P1.3.2.1.8",
          "target": "SS1.3.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 297,
          "source": "S1.3.3",
          "target": "T1.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 298,
          "source": "T1.4",
          "target": "CH1",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 299,
          "source": "S1.4.1",
          "target": "T1.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 300,
          "source": "SS1.4.1.1",
          "target": "S1.4.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 301,
          "source": "SS1.4.1.2",
          "target": "S1.4.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 302,
          "source": "SS1.4.1.3",
          "target": "S1.4.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 303,
          "source": "SS1.4.1.4",
          "target": "S1.4.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 304,
          "source": "S1.4.2",
          "target": "T1.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 305,
          "source": "SS1.4.2.1",
          "target": "S1.4.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 306,
          "source": "P1.4.2.1.1",
          "target": "SS1.4.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 307,
          "source": "P1.4.2.1.2",
          "target": "SS1.4.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 308,
          "source": "P1.4.2.1.3",
          "target": "SS1.4.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 309,
          "source": "P1.4.2.1.4",
          "target": "SS1.4.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 310,
          "source": "P1.4.2.1.5",
          "target": "SS1.4.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 311,
          "source": "P1.4.2.1.6",
          "target": "SS1.4.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 312,
          "source": "P1.4.2.1.7",
          "target": "SS1.4.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 313,
          "source": "T1.5",
          "target": "CH1",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 314,
          "source": "S1.5.1",
          "target": "T1.5",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 315,
          "source": "T1.6",
          "target": "CH1",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 316,
          "source": "T3.1",
          "target": "CH3",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 317,
          "source": "S3.1.1",
          "target": "T3.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 318,
          "source": "S3.1.2",
          "target": "T3.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 319,
          "source": "S3.1.2.1",
          "target": "S3.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 320,
          "source": "S3.1.2.2",
          "target": "S3.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 321,
          "source": "S3.1.2.3",
          "target": "S3.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 322,
          "source": "S3.1.2.4",
          "target": "S3.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 323,
          "source": "S3.1.2.5",
          "target": "S3.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 324,
          "source": "S3.1.3",
          "target": "T3.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 325,
          "source": "S3.1.4",
          "target": "T3.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 326,
          "source": "SS3.1.4.1",
          "target": "S3.1.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 327,
          "source": "SS3.1.4.2",
          "target": "S3.1.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 328,
          "source": "T3.2",
          "target": "CH3",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 329,
          "source": "S3.2.1",
          "target": "T3.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 330,
          "source": "S3.2.2",
          "target": "T3.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 331,
          "source": "T3.3",
          "target": "CH3",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 332,
          "source": "S3.3.1",
          "target": "T3.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 333,
          "source": "S3.3.2",
          "target": "T3.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 334,
          "source": "SS3.3.2.1",
          "target": "S3.3.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 335,
          "source": "SS3.3.2.2",
          "target": "S3.3.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 336,
          "source": "S3.3.3",
          "target": "T3.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 337,
          "source": "SS3.3.3.1",
          "target": "S3.3.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 338,
          "source": "SS3.3.3.2",
          "target": "S3.3.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 339,
          "source": "P3.3.3.2.1",
          "target": "SS3.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 340,
          "source": "P3.3.3.2.2",
          "target": "SS3.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 341,
          "source": "P3.3.3.2.3",
          "target": "SS3.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 342,
          "source": "P3.3.3.2.4",
          "target": "SS3.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 343,
          "source": "P3.3.3.2.5",
          "target": "SS3.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 344,
          "source": "P3.3.3.2.6",
          "target": "SS3.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 345,
          "source": "P3.3.3.2.7",
          "target": "SS3.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 346,
          "source": "T3.4",
          "target": "CH3",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 347,
          "source": "S3.4.1",
          "target": "T3.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 348,
          "source": "S3.4.2",
          "target": "T3.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 349,
          "source": "S3.4.3",
          "target": "T3.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 350,
          "source": "S3.4.4",
          "target": "T3.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 351,
          "source": "S3.4.5",
          "target": "T3.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 352,
          "source": "T3.5",
          "target": "CH3",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 353,
          "source": "S3.5.1",
          "target": "T3.5",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 354,
          "source": "SS3.5.1.1",
          "target": "S3.5.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 355,
          "source": "SS3.5.1.2",
          "target": "S3.5.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 356,
          "source": "P3.5.1.2.1",
          "target": "SS3.5.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 357,
          "source": "P3.5.1.2.2",
          "target": "SS3.5.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 358,
          "source": "P3.5.1.2.3",
          "target": "SS3.5.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 359,
          "source": "P3.5.1.2.4",
          "target": "SS3.5.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 360,
          "source": "S3.5.2",
          "target": "T3.5",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 361,
          "source": "SS3.5.2.1",
          "target": "S3.5.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 362,
          "source": "SS3.5.2.2",
          "target": "S3.5.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 363,
          "source": "P3.5.2.2.1",
          "target": "SS3.5.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 364,
          "source": "P3.5.2.2.2",
          "target": "SS3.5.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 365,
          "source": "P3.5.2.2.3",
          "target": "SS3.5.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 366,
          "source": "P3.5.2.2.4",
          "target": "SS3.5.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 367,
          "source": "P3.5.2.2.5",
          "target": "SS3.5.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 368,
          "source": "P3.5.2.2.6",
          "target": "SS3.5.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 369,
          "source": "SS3.5.2.3",
          "target": "S3.5.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 370,
          "source": "S3.5.3",
          "target": "T3.5",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 371,
          "source": "SS3.5.3.1",
          "target": "S3.5.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 372,
          "source": "SS3.5.3.2",
          "target": "S3.5.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 373,
          "source": "P3.5.3.2.1",
          "target": "SS3.5.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 374,
          "source": "P3.5.3.2.2",
          "target": "SS3.5.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 375,
          "source": "P3.5.3.2.3",
          "target": "SS3.5.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 376,
          "source": "P3.5.3.2.4",
          "target": "SS3.5.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 377,
          "source": "P3.5.3.2.5",
          "target": "SS3.5.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 378,
          "source": "T3.6",
          "target": "CH3",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 379,
          "source": "T6.1",
          "target": "CH6",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 380,
          "source": "S6.1.1",
          "target": "T6.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 381,
          "source": "SS6.1.1.1",
          "target": "S6.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 382,
          "source": "SS6.1.1.2",
          "target": "S6.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 383,
          "source": "P6.1.1.2.1",
          "target": "SS6.1.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 384,
          "source": "P6.1.1.2.2",
          "target": "SS6.1.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 385,
          "source": "P6.1.1.2.3",
          "target": "SS6.1.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 386,
          "source": "P6.1.1.2.4",
          "target": "SS6.1.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 387,
          "source": "P6.1.1.2.5",
          "target": "SS6.1.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 388,
          "source": "P6.1.1.2.6",
          "target": "SS6.1.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 389,
          "source": "P6.1.1.2.7",
          "target": "SS6.1.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 390,
          "source": "P6.1.1.2.8",
          "target": "SS6.1.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 391,
          "source": "S6.1.2",
          "target": "T6.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 392,
          "source": "SS6.1.2.1",
          "target": "S6.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 393,
          "source": "SS6.1.2.2",
          "target": "S6.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 394,
          "source": "P6.1.2.2.1",
          "target": "SS6.1.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 395,
          "source": "P6.1.2.2.2",
          "target": "SS6.1.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 396,
          "source": "P6.1.2.2.3",
          "target": "SS6.1.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 397,
          "source": "P6.1.2.2.4",
          "target": "SS6.1.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 398,
          "source": "P6.1.2.2.5",
          "target": "SS6.1.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 399,
          "source": "P6.1.2.2.6",
          "target": "SS6.1.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 400,
          "source": "P6.1.2.2.7",
          "target": "SS6.1.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 401,
          "source": "P6.1.2.2.8",
          "target": "SS6.1.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 402,
          "source": "T6.2",
          "target": "CH6",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 403,
          "source": "S6.2.1",
          "target": "T6.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 404,
          "source": "SS6.2.1.1",
          "target": "S6.2.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 405,
          "source": "SS6.2.1.2",
          "target": "S6.2.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 406,
          "source": "P6.2.1.2.1",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 407,
          "source": "P6.2.1.2.2",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 408,
          "source": "P6.2.1.2.3",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 409,
          "source": "P6.2.1.2.4",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 410,
          "source": "P6.2.1.2.5",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 411,
          "source": "P6.2.1.2.6",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 412,
          "source": "P6.2.1.2.7",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 413,
          "source": "P6.2.1.2.8",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 414,
          "source": "P6.2.1.2.9",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 415,
          "source": "P6.2.1.2.10",
          "target": "SS6.2.1.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 416,
          "source": "S6.2.2",
          "target": "T6.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 417,
          "source": "SS6.2.2.1",
          "target": "S6.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 418,
          "source": "SS6.2.2.2",
          "target": "S6.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 419,
          "source": "P6.2.2.2.1",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 420,
          "source": "P6.2.2.2.2",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 421,
          "source": "P6.2.2.2.3",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 422,
          "source": "P6.2.2.2.4",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 423,
          "source": "P6.2.2.2.5",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 424,
          "source": "P6.2.2.2.6",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 425,
          "source": "P6.2.2.2.7",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 426,
          "source": "P6.2.2.2.8",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 427,
          "source": "P6.2.2.2.9",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 428,
          "source": "P6.2.2.2.10",
          "target": "SS6.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 429,
          "source": "S6.2.3",
          "target": "T6.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 430,
          "source": "SS6.2.3.1",
          "target": "S6.2.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 431,
          "source": "SS6.2.3.2",
          "target": "S6.2.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 432,
          "source": "P6.2.3.2.1",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 433,
          "source": "P6.2.3.2.2",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 434,
          "source": "P6.2.3.2.3",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 435,
          "source": "P6.2.3.2.4",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 436,
          "source": "P6.2.3.2.5",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 437,
          "source": "P6.2.3.2.6",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 438,
          "source": "P6.2.3.2.7",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 439,
          "source": "P6.2.3.2.8",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 440,
          "source": "P6.2.3.2.9",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 441,
          "source": "P6.2.3.2.10",
          "target": "SS6.2.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 442,
          "source": "S6.2.4",
          "target": "T6.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 443,
          "source": "SS6.2.4.1",
          "target": "S6.2.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 444,
          "source": "SS6.2.4.2",
          "target": "S6.2.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 445,
          "source": "P6.2.4.2.1",
          "target": "SS6.2.4.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 446,
          "source": "P6.2.4.2.2",
          "target": "SS6.2.4.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 447,
          "source": "P6.2.4.2.3",
          "target": "SS6.2.4.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 448,
          "source": "SS6.2.4.3",
          "target": "S6.2.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 449,
          "source": "P6.2.4.3.1",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 450,
          "source": "P6.2.4.3.2",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 451,
          "source": "P6.2.4.3.3",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 452,
          "source": "P6.2.4.3.4",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 453,
          "source": "P6.2.4.3.5",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 454,
          "source": "P6.2.4.3.6",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 455,
          "source": "P6.2.4.3.7",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 456,
          "source": "P6.2.4.3.8",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 457,
          "source": "P6.2.4.3.9",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 458,
          "source": "P6.2.4.3.10",
          "target": "SS6.2.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 459,
          "source": "S6.2.5",
          "target": "T6.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 460,
          "source": "SS6.2.5.1",
          "target": "S6.2.5",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 461,
          "source": "SS6.2.5.2",
          "target": "S6.2.5",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 462,
          "source": "P6.2.5.2.1",
          "target": "SS6.2.5.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 463,
          "source": "P6.2.5.2.2",
          "target": "SS6.2.5.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 464,
          "source": "P6.2.5.2.3",
          "target": "SS6.2.5.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 465,
          "source": "P6.2.5.2.4",
          "target": "SS6.2.5.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 466,
          "source": "P6.2.5.2.5",
          "target": "SS6.2.5.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 467,
          "source": "T6.3",
          "target": "CH6",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 468,
          "source": "T8.1",
          "target": "CH8",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 469,
          "source": "S8.1.1",
          "target": "T8.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 470,
          "source": "SS8.1.1.1",
          "target": "S8.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 471,
          "source": "SS8.1.1.2",
          "target": "S8.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 472,
          "source": "S8.1.2",
          "target": "T8.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 473,
          "source": "SS8.1.2.1",
          "target": "S8.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 474,
          "source": "SS8.1.2.2",
          "target": "S8.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 475,
          "source": "SS8.1.2.3",
          "target": "S8.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 476,
          "source": "SS8.1.2.4",
          "target": "S8.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 477,
          "source": "SS8.1.2.5",
          "target": "S8.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 478,
          "source": "SS8.1.2.6",
          "target": "S8.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 479,
          "source": "S8.1.3",
          "target": "T8.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 480,
          "source": "SS8.1.3.1",
          "target": "S8.1.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 481,
          "source": "SS8.1.3.2",
          "target": "S8.1.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 482,
          "source": "SS8.1.3.3",
          "target": "S8.1.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 483,
          "source": "SS8.1.3.4",
          "target": "S8.1.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 484,
          "source": "SS8.1.3.5",
          "target": "S8.1.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 485,
          "source": "T8.2",
          "target": "CH8",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 486,
          "source": "S8.2.1",
          "target": "T8.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 487,
          "source": "SS8.2.1.1",
          "target": "S8.2.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 488,
          "source": "SS8.2.1.2",
          "target": "S8.2.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 489,
          "source": "S8.2.2",
          "target": "T8.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 490,
          "source": "SS8.2.2.1",
          "target": "S8.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 491,
          "source": "SS8.2.2.2",
          "target": "S8.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 492,
          "source": "P8.2.2.2.1",
          "target": "SS8.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 493,
          "source": "P8.2.2.2.2",
          "target": "SS8.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 494,
          "source": "P8.2.2.2.3",
          "target": "SS8.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 495,
          "source": "P8.2.2.2.4",
          "target": "SS8.2.2.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 496,
          "source": "S8.2.3",
          "target": "T8.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 497,
          "source": "SS8.2.3.1",
          "target": "S8.2.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 498,
          "source": "SS8.2.3.2",
          "target": "S8.2.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 499,
          "source": "SS8.2.3.3",
          "target": "S8.2.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 500,
          "source": "T8.3",
          "target": "CH8",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 501,
          "source": "S8.3.1",
          "target": "T8.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 502,
          "source": "SS8.3.1.1",
          "target": "S8.3.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 503,
          "source": "SS8.3.1.2",
          "target": "S8.3.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 504,
          "source": "S8.3.2",
          "target": "T8.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 505,
          "source": "SS8.3.2.1",
          "target": "S8.3.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 506,
          "source": "SS8.3.2.2",
          "target": "S8.3.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 507,
          "source": "S8.3.3",
          "target": "T8.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 508,
          "source": "S8.3.4",
          "target": "T8.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 509,
          "source": "SS8.3.4.1",
          "target": "S8.3.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 510,
          "source": "SS8.3.4.2",
          "target": "S8.3.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 511,
          "source": "SS8.3.4.3",
          "target": "S8.3.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 512,
          "source": "P8.3.4.3.1",
          "target": "SS8.3.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 513,
          "source": "P8.3.4.3.2",
          "target": "SS8.3.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 514,
          "source": "P8.3.4.3.3",
          "target": "SS8.3.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 515,
          "source": "P8.3.4.3.4",
          "target": "SS8.3.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 516,
          "source": "P8.3.4.3.5",
          "target": "SS8.3.4.3",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 517,
          "source": "SS8.3.4.4",
          "target": "S8.3.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 518,
          "source": "SS8.3.4.5",
          "target": "S8.3.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 519,
          "source": "T8.4",
          "target": "CH8",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 520,
          "source": "S8.4.1",
          "target": "T8.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 521,
          "source": "S8.4.2",
          "target": "T8.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 522,
          "source": "S8.4.3",
          "target": "T8.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 523,
          "source": "T8.5",
          "target": "CH8",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 524,
          "source": "S8.5.1",
          "target": "T8.5",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 525,
          "source": "S8.5.2",
          "target": "T8.5",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 526,
          "source": "S8.5.3",
          "target": "T8.5",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 527,
          "source": "S8.5.4",
          "target": "T8.5",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 528,
          "source": "SS8.5.4.1",
          "target": "S8.5.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 529,
          "source": "SS8.5.4.2",
          "target": "S8.5.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 530,
          "source": "T8.6",
          "target": "CH8",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 531,
          "source": "T15.1",
          "target": "CH15",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 532,
          "source": "S15.1.1",
          "target": "T15.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 533,
          "source": "SS15.1.1.1",
          "target": "S15.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 534,
          "source": "SS15.1.1.2",
          "target": "S15.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 535,
          "source": "SS15.1.1.3",
          "target": "S15.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 536,
          "source": "SS15.1.1.4",
          "target": "S15.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 537,
          "source": "SS15.1.1.5",
          "target": "S15.1.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 538,
          "source": "S15.1.2",
          "target": "T15.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 539,
          "source": "SS15.1.2.1",
          "target": "S15.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 540,
          "source": "SS15.1.2.2",
          "target": "S15.1.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 541,
          "source": "S15.1.3",
          "target": "T15.1",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 542,
          "source": "T15.2",
          "target": "CH15",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 543,
          "source": "S15.2.1",
          "target": "T15.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 544,
          "source": "SS15.2.1.1",
          "target": "S15.2.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 545,
          "source": "SS15.2.1.2",
          "target": "S15.2.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 546,
          "source": "SS15.2.1.3",
          "target": "S15.2.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 547,
          "source": "S15.2.2",
          "target": "T15.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 548,
          "source": "SS15.2.2.1",
          "target": "S15.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 549,
          "source": "P15.2.2.1.1",
          "target": "SS15.2.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 550,
          "source": "P15.2.2.1.2",
          "target": "SS15.2.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 551,
          "source": "P15.2.2.1.3",
          "target": "SS15.2.2.1",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 552,
          "source": "SS15.2.2.2",
          "target": "S15.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 553,
          "source": "SS15.2.2.3",
          "target": "S15.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 554,
          "source": "SS15.2.2.4",
          "target": "S15.2.2",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 555,
          "source": "S15.2.3",
          "target": "T15.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 556,
          "source": "S15.2.4",
          "target": "T15.2",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 557,
          "source": "T15.3",
          "target": "CH15",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 558,
          "source": "S15.3.1",
          "target": "T15.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 559,
          "source": "S15.3.2",
          "target": "T15.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 560,
          "source": "S15.3.3",
          "target": "T15.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 561,
          "source": "SS15.3.3.1",
          "target": "S15.3.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 562,
          "source": "SS15.3.3.2",
          "target": "S15.3.3",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 563,
          "source": "P15.3.3.2.1",
          "target": "SS15.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 564,
          "source": "P15.3.3.2.2",
          "target": "SS15.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 565,
          "source": "P15.3.3.2.3",
          "target": "SS15.3.3.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 566,
          "source": "S15.3.4",
          "target": "T15.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 567,
          "source": "SS15.3.4.1",
          "target": "S15.3.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 568,
          "source": "SS15.3.4.2",
          "target": "S15.3.4",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 569,
          "source": "S15.3.5",
          "target": "T15.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 570,
          "source": "S15.3.6",
          "target": "T15.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 571,
          "source": "SS15.3.6.1",
          "target": "S15.3.6",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 572,
          "source": "SS15.3.6.2",
          "target": "S15.3.6",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 573,
          "source": "S15.3.7",
          "target": "T15.3",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 574,
          "source": "SS15.3.7.1",
          "target": "S15.3.7",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 575,
          "source": "SS15.3.7.2",
          "target": "S15.3.7",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 576,
          "source": "P15.3.7.2.1",
          "target": "SS15.3.7.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 577,
          "source": "P15.3.7.2.2",
          "target": "SS15.3.7.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 578,
          "source": "P15.3.7.2.3",
          "target": "SS15.3.7.2",
          "relation": "Belong_SS",
          "value": 1
      },
      {
          "id": 579,
          "source": "T15.4",
          "target": "CH15",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 580,
          "source": "S15.4.1",
          "target": "T15.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 581,
          "source": "SS15.4.1.1",
          "target": "S15.4.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 582,
          "source": "SS15.4.1.2",
          "target": "S15.4.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 583,
          "source": "SS15.4.1.3",
          "target": "S15.4.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 584,
          "source": "SS15.4.1.4",
          "target": "S15.4.1",
          "relation": "Belong_ST",
          "value": 1
      },
      {
          "id": 585,
          "source": "S15.4.2",
          "target": "T15.4",
          "relation": "Belong_TP",
          "value": 1
      },
      {
          "id": 586,
          "source": "T15.5",
          "target": "CH15",
          "relation": "Belong_SB",
          "value": 1
      },
      {
          "id": 587,
          "source": "CH1",
          "target": "root",
          "relation": "Belong_root",
          "value": 1
      },
      {
          "id": 588,
          "source": "CH3",
          "target": "root",
          "relation": "Belong_root",
          "value": 1
      },
      {
          "id": 589,
          "source": "CH6",
          "target": "root",
          "relation": "Belong_root",
          "value": 1
      },
      {
          "id": 590,
          "source": "CH8",
          "target": "root",
          "relation": "Belong_root",
          "value": 1
      },
      {
          "id": 591,
          "source": "CH15",
          "target": "root",
          "relation": "Belong_root",
          "value": 1
      }

  ];

  // 设置除根节点外的所有节点和边的 visible 属性为 false
  this.nodes.forEach(node => {
    if (node.id !== 'root') { // 跳过根节点
      node.visible = false;
    }
  });
  this.tempEdges.forEach(edge => {
    edge.visible = false; // 默认所有边不可见
  });

  this.nodesMap = this.genNodesMap(this.nodes);
  this.nodesData = Object.values(this.nodesMap);
  this.linkMap = this.genLinkMap(this.tempEdges);
  this.edges = this.genLinks(this.tempEdges);
},
    initGraph() {
      this.svg = d3.select(this.$refs.d3Container)
        .append('svg')
        .attr('width', this.width)
        .attr('height', this.height);


      this.g = this.svg.append('g');
    this.zoom = d3.zoom()
    .on('zoom', (event) => {
      this.g.attr('transform', event.transform);
    });

  this.svg.call(this.zoom);

      this.forceSimulation = d3.forceSimulation(this.nodesData)
        .force('link', d3.forceLink(this.edges).id(d => d.id).distance(d => d.value * 200))
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(this.width / 2, this.height / 2));

        this.g.append('svg:defs').selectAll('marker')
        .data(['end'])      // 定义一个名为"end"的marker
        .enter().append('svg:marker')    // 创建marker元素
        .attr('id', d => d) // 修正这里
        .attr('viewBox', '0 -5 10 10')
        .attr('refX', 44)
        .attr('refY', 0)
        .attr('markerWidth', 10)
        .attr('markerHeight', 10)
        .attr('orient', 'auto')
        .append('svg:path')
        .attr('d', 'M0,-5L10,0L0,5')
        .attr('fill', '#000000');

      this.links = this.g.append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(this.edges)
        .enter()
        .append('line')
        .attr('stroke-width', d => Math.sqrt(d.value))
        .style('stroke', '#999')
        .attr('marker-end', 'url(#end)')
        .attr('visibility', d => d.visible ? 'visible' : 'hidden');

      this.linksText = this.g.append('g')
        .selectAll('text')
        .data(this.edges)
        .enter()
        .append('text')
        .attr('class', 'linksText')
        .text(d => d.relation)
        .style('font-size', 14)
        .attr('fill-opacity', 0)
        .attr('visibility', d => d.visible ? 'visible' : 'hidden');

        this.gs = this.g.append('g')
.selectAll('.circleText')
.data(this.nodesData)
.enter()
.append('g')
.attr('class', 'singleNode')
.attr('id', d => 'singleNode' + d.id)
.style('cursor', 'pointer')
.attr('visibility', d => d.visible ? 'visible' : 'hidden');

// 圆形节点的样式
this.gs.append('circle')
.attr('r', d => (20 + (d.name.split(' ')[0].split('.')).length * -3))
.style('fill', d => colors[(d.name.split(' ')[0].split('.')).length - 1])
.style('stroke', '#333') // 设置圆形边框颜色
.style('stroke-width', 2) // 设置圆形边框宽度
.style('transition', 'all 0.3s ease') // 设置平滑过渡效果


// 悬浮时改变圆形的大小、阴影和颜色
.on('mouseover', function() {
  d3.select(this)
    .style('fill', '#ff6347') // 悬浮时改变填充颜色
    .style('r', d => (25 + (d.name.split(' ')[0].split('.')).length * -3)) // 悬浮时增大圆形
    .style('filter', 'url(#shadow)'); // 添加阴影效果
})
.on('mouseout', function() {
  d3.select(this)
    .style('fill', d => colors[(d.name.split(' ')[0].split('.')).length - 1]) // 悬浮取消时恢复填充颜色
    .style('r', d => (20 + (d.name.split(' ')[0].split('.')).length * -3)) // 恢复圆形大小
    .style('filter', 'none'); // 移除阴影
})
.on('click', function() {
  // 点击时修改选中节点的样式
  d3.selectAll('.singleNode')
    .select('circle')
    .style('stroke', '#333') // 恢复所有圆形边框颜色
    .style('stroke-width', 2);

  d3.select(this)
    .select('circle')
    .style('stroke', '#00bcd4') // 设置选中节点边框颜色
    .style('stroke-width', 4); // 增大选中节点的边框宽度
})
.on('dblclick', (event, d) => {
      this.selectedNode = d; // 设置选中的节点
      this.selectedNode.content = this.findNodeContentById(this.selectedNode.id);
      this.drawerVisible = true; // 显示 drawer
    });

// 定义阴影效果
this.g.append('defs')
.append('filter')
.attr('id', 'shadow')
.append('feDropShadow')
.attr('dx', 0)
.attr('dy', 0)
.attr('stdDeviation', 5) // 阴影模糊程度
.attr('flood-color', '#888'); // 阴影颜色


      this.gs.append('text')
        .attr('dx', 20)
        .attr('dy', '.35em')
        .text(d => d.name);

      this.gs.call(d3.drag()
        .on('start', (event, d) => this.started(d, event))
        .on('drag', (event, d) => this.dragged(d, event))
        .on('end', (event, d) => this.ended(d, event)));

      this.forceSimulation.on('tick', () => this.ticked());
      this.gs.on('click', (event, d) => {event.stopPropagation(); // 阻止事件冒泡
        this.showMenu(event, d);
      });
      this.svg.on('click', () => this.hideMenu());//点击空白处隐藏菜单事件
    },
    findNodeContentById(nodeId) {
    // 遍历 response 数据，查找与 nodeId 匹配的节点内容
    for (const item of this.response) {
      if (item.start_properties.id === nodeId) {
        return item.start_properties.content;
      }
    }
    for (const item of this.response) {
      if (item.end_properties.id === nodeId) {
        return item.end_properties.content;
      }
    }
    return null;
  },
    showMenu(event, node) {
  // 隐藏之前的菜单
  this.hideMenu();

  // 获取 SVG 的偏移量
  const svgRect = this.svg.node().getBoundingClientRect();

  // 计算相对于 SVG 的坐标
  const svgX = event.clientX - svgRect.left;
  const svgY = event.clientY - svgRect.top;

  // 设置菜单的位置
  this.menuX = svgX;
  this.menuY = svgY;

  // 显示菜单
  this.menuVisible = true;

  const menu = this.svg.append('g')
    .attr('class', 'menu')
    .attr('transform', `translate(${this.menuX},${this.menuY})`);

  // 添加菜单背景
  menu.append('rect')
    .attr('width', 120)
    .attr('height', 100)
    .attr('rx', 5)
    .attr('ry', 5)
    .style('fill', '#fff')
    .style('stroke', '#000');

  // 添加按钮
  const buttonGroup = menu.append('g')
    .attr('class', 'buttons');

  this.buttons.forEach((button, index) => {
    const buttonY = 10 + index * 30; // 每个按钮间隔 30px

    // 添加按钮背景
    buttonGroup.append('rect')
      .attr('x', 10)
      .attr('y', buttonY)
      .attr('width', 100)
      .attr('height', 25)
      .attr('rx', 5)
      .attr('ry', 5)
      .style('fill', '#f0f0f0')
      .style('stroke', '#ccc')
      .style('cursor', 'pointer')
      .on('click', () => this.handleButtonClick(button.action, node)); // 绑定点击事件

    // 添加按钮文本
    buttonGroup.append('text')
      .text(button.text)
      .attr('x', 60)
      .attr('y', buttonY + 18)
      .style('font-size', 14)
      .style('text-anchor', 'middle')
      .style('cursor', 'pointer')
      .on('click', () => this.handleButtonClick(button.action, node)); // 绑定点击事件
  });

  console.log(node);
},

hideMenu() {
  // 移除菜单组
  this.svg.selectAll('.menu').remove();
  this.menuVisible = false;
},

handleButtonClick(action, node) { // 按钮点击事件处理函数
    console.log(`点击了按钮: ${action}`);
    console.log('当前节点:', node);

    // 根据 action 执行不同的操作
    switch (action) {
      case 'action1':
      this.collapseNode(node);
        break;
      case 'action2':
      this.expandNode(node);
        break;
      case 'action3':
        alert('按钮3被点击');
        break;
      default:
        console.warn('未知的按钮操作');
    }
  },
    genNodesMap(nodes) {
      const hash = {};
      nodes.forEach(node => {
        hash[node.id] = { id: node.id, name: node.name };
      });
      return hash;
    },
    genLinkMap(tempEdges) {
      const hash = {};
      tempEdges.forEach(edge => {
        const key = edge.source + '-' + edge.target;
        if (hash[key]) {
          hash[key] += 1;
          hash[key + '-relation'] += '、' + edge.relation;
        } else {
          hash[key] = 1;
          hash[key + '-relation'] = edge.relation;
        }
      });
      return hash;
    },
    genLinks(tempEdges) {
      const indexHash = {};
      return tempEdges.map(edge => {
        const linkKey = edge.source + '-' + edge.target;
        const count = this.linkMap[linkKey];
        if (indexHash[linkKey]) {
          indexHash[linkKey] -= 1;
        } else {
          indexHash[linkKey] = count - 1;
        }
        return {
          ...edge,
          source: this.nodesMap[edge.source],
          target: this.nodesMap[edge.target],
          relations: this.linkMap[linkKey + '-relation'],
          count: this.linkMap[linkKey],
          index: indexHash[linkKey],
        };
      });
    },
    showAllNodes() {
    // 将所有节点的 visible 属性设置为 true
    this.nodesData.forEach(node => {
      node.visible = true;
    });

    // 将所有边的 visible 属性设置为 true
    this.edges.forEach(edge => {
      edge.visible = true;
    });

    // 更新图形的显示
    this.updateGraph();
  },

  updateGraph() {
    // 更新节点的显示
    this.gs.attr('visibility', d => d.visible ? 'visible' : 'hidden');

    // 更新边的显示
    this.links.attr('visibility', d => d.visible ? 'visible' : 'hidden');
    this.linksText.attr('visibility', d => d.visible ? 'visible' : 'hidden');
  },



  collapseNode(node) {
  // 获取以当前节点为终点的所有边
  const edgesToHide = this.edges.filter(edge => edge.target.id === node.id && edge.relation !== 'Next_ST' && edge.relation !== 'Next_TP' && edge.relation !== 'Next_SB' && edge.relation !== 'Next_P' && edge.relation !== 'Next_SS');

  // 隐藏这些边
  edgesToHide.forEach(edge => {
    edge.visible = false; // 更新边的 visible 属性
    this.hideEdge(edge);
  });

  // 隐藏这些边的起点节点，并递归隐藏以这些节点为终点的边和节点
  edgesToHide.forEach(edge => {
    const sourceNode = edge.source;
    this.hideNodeRecursive(sourceNode);
  });
},

hideNodeRecursive(node) {
  // 如果节点已经是隐藏的，直接返回
  if (!node.visible) return;

  // 隐藏当前节点
  node.visible = false;
  this.hideNode(node);

  // 获取以当前节点为终点的所有边
  const edgesToHide = this.edges.filter(edge => edge.target.id === node.id);

  // 隐藏这些边
  edgesToHide.forEach(edge => {
    edge.visible = false;
    this.hideEdge(edge);
  });

  // 递归隐藏这些边的起点节点
  edgesToHide.forEach(edge => {
    const sourceNode = edge.source;
    this.hideNodeRecursive(sourceNode);
  });
},

hideEdge(edge) {
  edge.visible = false;
  this.links.filter(d => d === edge).attr('visibility', 'hidden');
  this.linksText.filter(d => d === edge).attr('visibility', 'hidden');
},

hideNode(node) {
  node.visible = false;
  this.gs.filter(d => d.id === node.id).attr('visibility', 'hidden');
},


expandNode(node) {
  // 获取以当前节点为终点的所有边，并且这些边当前是隐藏的
  const edgesToShow = this.edges.filter(edge => edge.target.id === node.id && !edge.visible);

  // 显示这些边
  edgesToShow.forEach(edge => {
    edge.visible = true; // 更新边的 visible 属性
    this.showEdge(edge);
  });

  // 显示这些边的起点节点
  edgesToShow.forEach(edge => {
    const sourceNode = edge.source;
    sourceNode.visible = true; // 更新节点的 visible 属性
    this.showNode(sourceNode);
  });
},

showEdge(edge) {
  edge.visible = true; // 更新边的 visible 属性
  this.links.filter(d => d === edge).attr('visibility', 'visible');
  this.linksText.filter(d => d === edge).attr('visibility', 'visible');
},

showNode(node) {
  node.visible = true; // 更新节点的 visible 属性
  this.gs.filter(d => d.id === node.id).attr('visibility', 'visible');
},
    genLinkPath(link) {
      return `M${link.source.x},${link.source.y} L${link.target.x},${link.target.y}`;
    },
    started(d, event) {
      if (!event.active) {
        this.forceSimulation.alphaTarget(0.8).restart();
      }
      d.fx = d.x;
      d.fy = d.y;
    },
    dragged(d, event) {
      d.fx = event.x;
      d.fy = event.y;
    },
    ended(d, event) {
      if (!event.active) {
        this.forceSimulation.alphaTarget(0);
      }
      d.fx = null;
      d.fy = null;
    },
    ticked() {
    this.links
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)
      .attr('visibility', d => d.visible ? 'visible' : 'hidden');

    this.linksText
      .attr('x', d => (d.source.x + d.target.x) / 2)
      .attr('y', d => (d.source.y + d.target.y) / 2)
      .attr('visibility', d => d.visible ? 'visible' : 'hidden');

    this.gs
      .attr('transform', d => `translate(${d.x},${d.y})`)
      .attr('visibility', d => d.visible ? 'visible' : 'hidden');
  },
  handleAction(action) {
      if (action === 'action1') {
        this.Stayroot();
      }
    },
    Stayroot() {
      // 获取以当前节点为终点的所有边
    const edgesToHide = this.edges.filter(edge => edge.target.id === 'root');

    // 隐藏这些边
    edgesToHide.forEach(edge => {
    edge.visible = false; // 更新边的 visible 属性
    this.hideEdge(edge);
    });

    // 隐藏这些边的起点节点，并递归隐藏以这些节点为终点的边和节点
    edgesToHide.forEach(edge => {
    const sourceNode = edge.source;
    this.hideNodeRecursive(sourceNode);
    });
      console.log('Action 1 triggered!');
    }
  },
};
</script>

