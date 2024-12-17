<template>
  <div class="topology-card">
      <div class="scrollable-container">
        <svg id="topology" width="2000" height="1600"></svg>
      </div>
  </div>
</template>

<script>
import * as d3 from 'd3';

// 使用require导入JSON文件，确保路径正确
const data = require('@/components/.json');

export default {
name: "SoftwareEngineeringGraph",
data() {
  return {
    nodes: [],
    links: []
  };
},
mounted() {
  this.loadData();
  this.initGraph();
},
methods: {
  loadData() {
const allNodes = new Set();

data.forEach(item => {
  // 添加起始节点
  allNodes.add(item.start_id);
  // 添加结束节点
  allNodes.add(item.end_id);
});

// 创建节点数组
this.nodes = Array.from(allNodes).map(node => {
  // 根据节点ID查找对应的属性
  const startProperties = data.find(i => i.start_id === node)?.start_properties;
  const endProperties = data.find(i => i.end_id === node)?.end_properties;
  
  // 如果节点在起始节点和结束节点中都存在，则需要合并属性
  const properties = startProperties || endProperties;
  return {
    id: node,
    name: properties ? properties.name : node
  };
});

// 创建链接数组
this.links = data.map(item => ({
  source: item.start_id,
  target: item.end_id,
  relationship: item.relation
}));
},
  initGraph() {
    const svg = d3.select('#topology');
    const width = +svg.attr('width');
    const height = +svg.attr('height');
    //marker
    svg.append('defs').selectAll('marker')
      .data(this.links)
      .enter().append('marker')
      .attr('id', 'arrowhead')
      .attr('viewBox', '-0 -5 10 10')
      .attr('refX', 30)
      .attr('refY', 0)
      .attr('markerWidth', 10)
      .attr('markerHeight', 10)
      .attr('orient', 'auto')
      .append('svg:path')
      .attr('d', 'M 0,-5 L 10,0 L 0,5')
      .attr('fill', '#999');

    const simulation = d3.forceSimulation(this.nodes)
      .force('link', d3.forceLink(this.links).id(d => d.id).distance(150))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(width / 2, height / 2));

      const link = svg.selectAll('line')
      .data(this.links)
      .enter()
      .append('line')
      .attr('stroke', '#ccc')
      .attr('stroke-width', 1)
      .attr('marker-end', 'url(#arrowhead)');  // 设置箭头

    const linkText = svg.selectAll('.linkText')
      .data(this.links)
      .enter()
      .append('text')
      .style('fill', 'black')
      .text(d => d.relationship)
      .attr('font-size', '10px')
      .attr('text-anchor', 'middle')
      .attr('alignment-baseline', 'middle');

    const node = svg.selectAll('circle')
      .data(this.nodes)
      .enter()
      .append('circle')
      .attr('r', 20)
      .attr('fill', 'red')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    const label = svg.selectAll('.label')
      .data(this.nodes)
      .enter()
      .append('text')
      .attr('class', "label")
      .text(d => d.name.split(' ')[0])
      .attr("dx", -8)
      .attr("dy", ".35em");
      label.style("font-size", "8px");  // 调整字体大小
    node.append('title')
      .text(d => d.name);

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      linkText
        .attr('x', d => (d.source.x + d.target.x) / 2)
        .attr('y', d => (d.source.y + d.target.y) / 2);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
      label
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.1).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
  }
}
}
</script>

<style scoped>
 
.topology-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.1);
  padding: 25px;
  width: 95%;
}

.topology-description {
  font-family: 'Arial', sans-serif;
  color: #666;
  font-size: 16px;
  margin-bottom: 25px;
}

.scrollable-container {
  overflow: auto; /* 允许滚动 */
  width: 100%; /* 确保滚动容器填满 svg-container */
  height: 85vh; /* 根据需要调整高度 */
}


line {
  transition: stroke-dashoffset 0.5s ease;
}

.label {
  font-family: 'Verdana', sans-serif;
  font-size: 12px;
  fill: #4a4a4a;
}
</style>
